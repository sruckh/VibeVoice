import runpod
import os
import torch
import numpy as np
import base64
import io
import torchaudio
import copy
import subprocess
import uuid
import boto3
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, Optional, Tuple, cast

# Import necessary VibeVoice components
from vibevoice.modular.modeling_vibevoice_streaming_inference import VibeVoiceStreamingForConditionalGenerationInference
from vibevoice.processor.vibevoice_streaming_processor import VibeVoiceStreamingProcessor

# Set up cache directory for Hugging Face models
os.environ["HF_HOME"] = "/workspace/VibeVoice/cache"
os.environ["HUGGINGFACE_HUB_CACHE"] = "/workspace/VibeVoice/cache"

# --- Model Loading (Global Scope for Warm Starts) ---
processor = None
model = None
service = None 

DEFAULT_MODEL_PATH = "microsoft/VibeVoice-Realtime-0.5B"
DEFAULT_VOICE_PRESET = "en-Emma_woman"

class RunPodStreamingTTSService:
    def __init__(
        self,
        model_path: str = DEFAULT_MODEL_PATH,
        device: str = "cuda",
        inference_steps: int = 5,
        default_voice_key: str = DEFAULT_VOICE_PRESET
    ) -> None:
        self.model_path = Path(model_path)
        self.device = device
        self._torch_device = torch.device(device)
        self.inference_steps = inference_steps
        self.default_voice_key = default_voice_key

        self.processor: Optional[VibeVoiceStreamingProcessor] = None
        self.model: Optional[VibeVoiceStreamingForConditionalGenerationInference] = None
        self.voice_presets: Dict[str, Path] = {}
        self._voice_cache: Dict[str, Tuple[object, Path, str]] = {}

    def load_model(self) -> None:
        print(f"[RunPodService] Loading processor from {self.model_path}")
        self.processor = VibeVoiceStreamingProcessor.from_pretrained(str(self.model_path))

        load_dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        device_map = 'cuda' if self.device == "cuda" else 'cpu'
        attn_impl_primary = "flash_attention_2" if self.device == "cuda" else "sdpa"

        print(f"[RunPodService] Using device: {device_map}, torch_dtype: {load_dtype}, attn_implementation: {attn_impl_primary}")
        try:
            self.model = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained(
                str(self.model_path),
                torch_dtype=load_dtype,
                device_map=device_map,
                attn_implementation=attn_impl_primary,
            )
        except Exception as e:
            print(f"Error loading model with {attn_impl_primary}. Falling back to SDPA: {e}")
            self.model = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained(
                str(self.model_path),
                torch_dtype=load_dtype,
                device_map=device_map,
                attn_implementation='sdpa',
            )
            print("[RunPodService] Model loaded with SDPA successfully.")

        self.model.eval()
        self.model.model.noise_scheduler = self.model.model.noise_scheduler.from_config(
            self.model.model.noise_scheduler.config,
            algorithm_type="sde-dpmsolver++",
            beta_schedule="squaredcos_cap_v2",
        )
        self.model.set_ddpm_inference_steps(num_steps=self.inference_steps)
        self._load_voice_presets()
        self._ensure_voice_cached(self.default_voice_key)

    def _load_voice_presets(self) -> None:
        voices_dir = Path("./demo/voices/streaming_model")
        if not voices_dir.exists():
            raise RuntimeError(f"Voices directory not found: {voices_dir}")
        for pt_path in voices_dir.glob("*.pt"):
            self.voice_presets[pt_path.stem] = pt_path
        if not self.voice_presets:
            raise RuntimeError(f"No voice preset (.pt) files found in {voices_dir}")
        print(f"[RunPodService] Found {len(self.voice_presets)} voice presets.")
        if self.default_voice_key not in self.voice_presets:
            print(f"[RunPodService] Default voice {self.default_voice_key!r} not found, using first available.")
            self.default_voice_key = next(iter(self.voice_presets))

    def _ensure_voice_cached(self, key: str) -> Tuple[object, Path, str]:
        if key not in self.voice_presets:
            raise RuntimeError(f"Voice preset {key!r} not found.")
        if key not in self._voice_cache:
            preset_path = self.voice_presets[key]
            print(f"[RunPodService] Loading voice preset {key} from {preset_path}.")
            prefilled_outputs = torch.load(
                preset_path,
                map_location=self._torch_device,
                weights_only=False,
            )
            self._voice_cache[key] = prefilled_outputs
        return self._voice_cache[key]

    def infer(self, text: str, reference_audio_base64: str, voice_key: Optional[str] = None) -> bytes:
        if not self.processor or not self.model:
            raise RuntimeError("RunPodStreamingTTSService not initialized.")
        
        selected_voice_key = voice_key if voice_key and voice_key in self.voice_presets else self.default_voice_key
        _, prefilled_outputs = self._ensure_voice_cached(selected_voice_key)

        processor_kwargs = {
            "text": text.strip(),
            "cached_prompt": prefilled_outputs, 
            "padding": True,
            "return_tensors": "pt",
            "return_attention_mask": True,
        }

        inputs = self.processor.process_input_with_cached_prompt(**processor_kwargs)
        inputs = {k: v.to(self._torch_device) if hasattr(v, "to") else v for k, v in inputs.items()}

        generated_audio_waveform = self.model.generate(
            **inputs,
            max_new_tokens=None,
            cfg_scale=1.5,
            tokenizer=self.processor.tokenizer,
            generation_config={
                "do_sample": False,
                "temperature": 1.0,
                "top_p": 1.0,
            },
            verbose=False,
            refresh_negative=True,
            all_prefilled_outputs=copy.deepcopy(prefilled_outputs),
        )

        generated_audio_waveform = generated_audio_waveform.detach().cpu().numpy().flatten()
        TARGET_SAMPLE_RATE = 24000
        audio_output_buffer = io.BytesIO()
        torchaudio.save(audio_output_buffer, torch.from_numpy(generated_audio_waveform).unsqueeze(0), TARGET_SAMPLE_RATE, format="wav")
        audio_output_buffer.seek(0)
        return audio_output_buffer.getvalue()

def convert_audio(wav_bytes: bytes, output_format: str = "mp3") -> bytes:
    """Converts WAV bytes to the target format using ffmpeg."""
    if output_format == "wav":
        return wav_bytes
    
    try:
        process = subprocess.Popen(
            ['ffmpeg', '-i', 'pipe:0', '-f', output_format, 'pipe:1'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate(input=wav_bytes)
        if process.returncode != 0:
            print(f"FFmpeg error: {err.decode('utf-8')}")
            raise RuntimeError(f"FFmpeg conversion failed: {err.decode('utf-8')}")
        return out
    except Exception as e:
        print(f"Audio conversion failed: {e}")
        raise

def upload_to_s3(audio_bytes: bytes, extension: str) -> str:
    """Uploads audio bytes to S3 and returns a presigned URL."""
    bucket_name = os.environ.get('BUCKET_NAME')
    endpoint_url = os.environ.get('BUCKET_ENDPOINT_URL')
    
    if not bucket_name:
        raise ValueError("BUCKET_NAME env var not set")

    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    
    filename = f"{uuid.uuid4()}.{extension}"
    s3.put_object(Bucket=bucket_name, Key=filename, Body=audio_bytes)
    
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': filename},
        ExpiresIn=3600 # 1 hour expiration
    )
    return url

def init():
    global service
    print("[RunPod Handler] Initializing VibeVoice service...")
    service = RunPodStreamingTTSService(
        model_path=os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH),
        device=os.environ.get("MODEL_DEVICE", "cuda"),
        inference_steps=int(os.environ.get("INFERENCE_STEPS", "5"))
    )
    service.load_model()
    print("[RunPod Handler] VibeVoice service initialized.")

async def handler(job):
    global service
    if service is None:
        await runpod.serverless.utils.rp_cuda.await_current_cuda_device_initialization()
        init()

    job_input = job['input']
    text_input = job_input.get('text')
    reference_audio_base64 = job_input.get('reference_audio')
    voice_key = job_input.get('voice_key', DEFAULT_VOICE_PRESET)
    output_format = job_input.get('output_format', 'mp3') # Default to mp3

    if not text_input:
        return {"error": "No text provided for TTS."}

    try:
        # Inference (returns WAV bytes)
        wav_bytes = service.infer(text_input, reference_audio_base64, voice_key)
        
        # Convert (if needed)
        final_audio_bytes = convert_audio(wav_bytes, output_format)
        
        # Check if S3 upload is configured
        bucket_name = os.environ.get('BUCKET_NAME')
        
        response = {
            "metadata": {
                "text_length": len(text_input),
                "voice_key": service.default_voice_key,
                "model_path": service.model_path.name,
                "format": output_format
            }
        }

        if bucket_name:
            # Upload to S3
            presigned_url = upload_to_s3(final_audio_bytes, output_format)
            response["audio_url"] = presigned_url
        else:
            # Return Base64
            response["audio_base64"] = base64.b64encode(final_audio_bytes).decode('utf-8')

        return response

    except Exception as e:
        print(f"Error during handler execution: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    init()
    runpod.serverless.start({"handler": handler})