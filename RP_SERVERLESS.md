# RunPod Serverless Deployment Plan for VibeVoice

## 1. Objective
Deploy the Microsoft VibeVoice TTS model as a serverless endpoint on RunPod. The deployment will utilize a network-attached volume (`/workspace`) to persist the model and code. The system will support audio compression (MP3/AAC) and optional cloud storage upload (S3/Backblaze) for generated audio files.

## 2. Architecture & Environment

*   **Platform:** RunPod Serverless.
*   **Base Image:** `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04` (defined in `Dockerfile`).
*   **System Dependencies:** `ffmpeg` (installed via Dockerfile) for audio compression.
*   **Storage:** Network Volume mounted at `/workspace`.
*   **Working Directory:** `/workspace/VibeVoice`.

### Environment Variables
The following environment variables should be configured in the RunPod Serverless settings:

*   `MODEL_PATH`: Path or HF ID for the VibeVoice model (default: `microsoft/VibeVoice-Realtime-0.5B`).
*   `MODEL_DEVICE`: Device to run inference on (default: `cuda`).
*   `INFERENCE_STEPS`: Number of inference steps (default: `5`).
*   `BUCKET_NAME`: (Optional) S3/Backblaze bucket name for storing audio.
*   `BUCKET_ENDPOINT_URL`: (Optional) S3-compatible endpoint URL (e.g., `https://s3.us-west-004.backblazeb2.com`). Region can be extracted or explicitly set if needed.
*   `AWS_ACCESS_KEY_ID`: (Optional) Access key for S3 storage.
*   `AWS_SECRET_ACCESS_KEY`: (Optional) Secret key for S3 storage.

## 3. Runtime Initialization (Bootstrap)

A master bootstrap script (`runpod_bootstrap.sh`) will run when the container starts.

1.  **Check Environment:** Verify if `/workspace/VibeVoice` exists and if a "setup_complete" marker file is present.
2.  **Storage Cleanup:** Check the configured S3 bucket (if enabled) and delete files older than 7 days to manage storage costs.
3.  **First-Run Installation (if marker is missing):**
    *   **Install `sage_attn`:** Install `flash-attn` wheel explicitly.
    *   **Clone Repository:** Clone `https://github.com/microsoft/VibeVoice.git` into `/workspace/VibeVoice`.
    *   **Modify pyproject.toml:** Remove `torch`, `torchvision`, `torchaudio` to preserve container's PyTorch.
    *   **Install Dependencies:** Run `pip install -e .` and install `boto3` (for S3 support).
    *   **Model Download Note:** Automatic via Hugging Face cache in `/workspace/VibeVoice/cache`.
    *   **Create Marker:** Create `.setup_complete`.
4.  **Launch Handler:** Start the RunPod serverless handler.

## 4. Serverless Handler (`handler.py`)

*   **Imports:** `runpod`, `torch`, `boto3` (if available), `subprocess` (for ffmpeg), VibeVoice modules.
*   **Model Loading:** Global loading for warm starts.
*   **Input Schema:**
    *   `text` (string): Text to be spoken.
    *   `reference_audio` (string): Base64/URL (Ignored for conditioning currently, using `voice_key`).
    *   `voice_key` (string): Voice preset to use.
    *   `output_format` (string): `mp3`, `aac`, or `wav` (default: `mp3`).
*   **Processing:**
    *   Run inference -> WAV numpy array.
    *   **Compression:** Convert WAV to requested format (MP3/AAC) using `ffmpeg`.
    *   **Delivery:**
        *   If S3 env vars are set: Upload file to bucket and generate a presigned URL.
        *   Otherwise: Return Base64 encoded audio string.
*   **Output Schema:**
    *   `audio_url` (string): Presigned URL (if S3 used).
    *   `audio_base64` (string): Base64 audio (if S3 not used).
    *   `metadata` (object): Generation stats.

## 5. Todo List

- [x] **Define Dockerfile**: Updated to include `ffmpeg`.
- [x] **Create `bootstrap.py` (or `.sh`)**:
    - [x] Runtime installation logic (sage_attn, git clone, deps).
    - [x] **Update**: Add `boto3` installation.
    - [x] **Update**: Add S3 cleanup logic (delete > 7 days).
- [x] **Create `handler.py`**:
    - [x] Basic inference logic.
    - [x] **Update**: Add `ffmpeg` compression logic.
    - [x] **Update**: Add S3 upload & presigned URL generation.
- [ ] **Test Locally**: Simulate bootstrap and inference.