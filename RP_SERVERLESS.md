# RunPod Serverless Deployment Plan for VibeVoice

## 1. Objective
Deploy the Microsoft VibeVoice TTS model as a serverless endpoint on RunPod. The deployment will utilize a network-attached volume (typically mounted at `/runpod-volume`) to persist the model, virtual environment, and code, ensuring fast warm starts and data persistence.

## 2. Architecture & Environment

*   **Platform:** RunPod Serverless.
*   **Base Image:** `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04` (defined in `Dockerfile`).
*   **System Dependencies:** `ffmpeg` (installed via Dockerfile) for audio compression.
*   **Storage:** Network Volume (`/runpod-volume`) or Ephemeral (`/workspace`).
*   **Project Root:** `/runpod-volume/VibeVoice` (Persistent) or `/workspace/VibeVoice` (Ephemeral).
    *   **Code:** Cloned into Project Root.
    *   **Venv:** `.../VibeVoice/venv`.
    *   **Cache:** `.../VibeVoice/cache`.

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

1.  **Volume Detection:** Checks for `/runpod-volume`. If present, sets it as the base; otherwise uses `/workspace`.
2.  **Venv Setup:** Creates/Activates a persistent virtual environment in `.../VibeVoice/venv`.
3.  **Storage Cleanup:** Checks the configured S3 bucket (if enabled) and deletes files older than 7 days.
4.  **First-Run Installation (if `.setup_complete` marker is missing):**
    *   **Install PyTorch:** Specific CUDA-optimized version.
    *   **Install `sage_attn`:** Flash Attention wheel.
    *   **Clone Repository:** Clones `https://github.com/sruckh/VibeVoice.git`. Uses `git init`/`reset` to handle cloning into a potentially non-empty directory.
    *   **Modify pyproject.toml:** Removes `torch` deps to prevent overwriting.
    *   **Install Dependencies:** Installs package and `boto3`.
    *   **Marker:** Creates `.setup_complete`.
5.  **Launch Handler:** Starts `handler.py` from the project root.

## 4. Serverless Handler (`handler.py`)

*   **Imports:** `runpod`, `torch`, `boto3`, `subprocess`, VibeVoice modules.
*   **Model Loading:** Global loading for warm starts.
*   **Input Schema:**
    *   `text` (string): Text to be spoken.
    *   `reference_audio` (string): Base64/URL (Ignored for conditioning currently, using `voice_key`).
    *   `voice_key` (string): Voice preset to use.
    *   `output_format` (string): `mp3`, `aac`, or `wav` (default: `mp3`).
*   **Processing:**
    *   Run inference -> WAV numpy array.
    *   **Compression:** Convert WAV to requested format using `ffmpeg`.
    *   **Delivery:**
        *   If S3 env vars set: Upload to bucket -> Presigned URL.
        *   Else: Return Base64 string.
*   **Output Schema:**
    *   `audio_url` (string) OR `audio_base64` (string).
    *   `metadata` (object): Stats & info.

## 5. Todo List

- [x] **Define Dockerfile**: Updated to include `ffmpeg`.
- [x] **Create `bootstrap.py` (or `.sh`)**:
    - [x] Runtime installation logic (sage_attn, git clone, deps).
    - [x] **Update**: Add `boto3` installation.
    - [x] **Update**: Add S3 cleanup logic (delete > 7 days).
    - [x] **Update**: Persistence logic (`/runpod-volume/VibeVoice`).
- [x] **Create `handler.py`**:
    - [x] Basic inference logic.
    - [x] **Update**: Add `ffmpeg` compression logic.
    - [x] **Update**: Add S3 upload & presigned URL generation.
- [ ] **Test Locally**: Simulate bootstrap and inference.
