# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🛑 STOP — Run codemap before ANY task

```bash
codemap .                     # Project structure
codemap --deps                # How files connect
codemap --diff                # What changed vs main
codemap --diff --ref <branch> # Changes vs specific branch
```

## Required Usage

**BEFORE starting any task**, run `codemap .` first.

**ALWAYS run `codemap --deps` when:**
- User asks how something works
- Refactoring or moving code
- Tracing imports or dependencies

**ALWAYS run `codemap --diff` when:**
- Reviewing or summarizing changes
- Before committing code
- User asks what changed
- Use `--ref <branch>` when comparing against something other than main

## Project Overview

VibeVoice is an open-source frontier voice AI framework for generating expressive, long-form, multi-speaker conversational audio from text. It includes:

1. **Long-form multi-speaker model**: Generates conversational speech up to 90 minutes with up to 4 distinct speakers
2. **Realtime streaming TTS model**: Produces initial audible speech in ~300ms with streaming text input support

### Core Architecture

- **Next-token diffusion framework**: Combines LLM for text understanding with diffusion head for acoustic details
- **Ultra-low frame rate tokenizers** (7.5 Hz): Continuous acoustic and semantic tokenizers for efficiency
- **Modular design** in `vibevoice/modular/`: Separate components for streaming inference, tokenizers, and diffusion heads
- **Processor pipeline** in `vibevoice/processor/`: Handles text tokenization and audio processing

### Key Components

- `vibevoice/modular/modeling_vibevoice_streaming_inference.py`: Core real-time inference model
- `vibevoice/modular/streamer.py`: Audio streaming functionality
- `vibevoice/processor/vibevoice_streaming_processor.py`: Streaming text/audio processor
- `vibevoice/schedule/dpm_solver.py`: Diffusion sampling algorithm
- Demo applications in `demo/web/`: WebSocket-based real-time TTS service

## Common Development Commands

### Installation
```bash
pip install -e .
```

### Running Real-time Demo
```bash
# Launch WebSocket demo server
python demo/vibevoice_realtime_demo.py --model_path microsoft/VibeVoice-Realtime-0.5B --port 3000

# Inference from files
python demo/realtime_model_inference_from_file.py \
    --model_path microsoft/VibeVoice-Realtime-0.5B \
    --txt_path demo/text_examples/1p_vibevoice.txt \
    --speaker_name Carter
```

### Model Configuration
- Model configs: `vibevoice/configs/qwen2.5_1.5b_64k.json`, `qwen2.5_7b_32k.json`
- Voice presets: `demo/voices/streaming_model/` (contains .pt files for different speakers)

### Dependencies
- PyTorch with CUDA/MPS support
- transformers==4.51.3 (specific version required)
- flash-attn (for optimal performance)
- FastAPI/Uvicorn for web demo
- librosa, numpy, scipy for audio processing

### Testing Model Loading
```python
from vibevoice.modular.modeling_vibevoice_streaming_inference import VibeVoiceStreamingForConditionalGenerationInference
from vibevoice.processor.vibevoice_streaming_processor import VibeVoiceStreamingProcessor

processor = VibeVoiceStreamingProcessor.from_pretrained("microsoft/VibeVoice-Realtime-0.5B")
model = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained(
    "microsoft/VibeVoice-Realtime-0.5B",
    torch_dtype=torch.bfloat16,
    device_map='cuda',
    attn_implementation="flash_attention_2"
)
```

## Architecture Notes

- Hub files: `modeling_vibevoice_streaming_inference`, `vibevoice_streaming_processor`, `modular_vibevoice_text_tokenizer`, `dpm_solver`
- Web demo uses WebSocket for real-time communication
- Model supports streaming text input with interleaved windowed design
- Single speaker only for realtime model (vs multi-speaker for long-form variant)
- Voice customization uses embedded format to mitigate deepfake risks