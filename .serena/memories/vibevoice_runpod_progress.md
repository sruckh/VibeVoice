# VibeVoice RunPod Serverless Deployment Progress

## Summary
The goal is to deploy Microsoft's VibeVoice TTS model as a serverless endpoint on RunPod, utilizing a persistent network volume (`/workspace`) to minimize cold start latency. We have implemented a complete deployment plan, including a Dockerfile, a runtime bootstrap script, and a serverless handler with advanced features like audio compression and cloud storage offloading.

## Decisions Made

1.  **Architecture:**
    *   **Platform:** RunPod Serverless.
    *   **Base Image:** `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04` (User specified).
    *   **Storage:** Network Volume mounted at `/workspace`. Code and models reside in `/workspace/VibeVoice`.
    *   **Dependencies:** Installed into a persistent virtual environment (`/workspace/venv`) to survive container restarts (ephemeral containers, persistent volume).

2.  **Runtime Logic (`runpod_bootstrap.sh`):**
    *   **Persistence:** Checks for a `.setup_complete` marker.
    *   **Dependency Management:** On first run, it installs `sage_attn` (Flash Attention via specific wheel), clones the repo, removes `torch` from `pyproject.toml` to protect the container's optimized PyTorch, and installs dependencies.
    *   **S3 Cleanup:** On *every* run, it attempts to clean up files older than 7 days from the configured S3 bucket (if `boto3` is available).

3.  **Inference Handler (`handler.py`):**
    *   **Audio Format:** Supports `mp3` (default), `aac`, and `wav`. Uses `ffmpeg` (installed in Dockerfile) for compression.
    *   **Delivery:** Can return a Presigned URL (if S3 env vars are set) or Base64 encoded string.
    *   **Conditioning:** *Caveat identified:* The current VibeVoice API relies on pre-tokenized voice presets (`.pt` files). The handler currently ignores the `reference_audio` input for direct conditioning and instead uses `voice_key` to select a preset.

4.  **Environment Variables:**
    *   `BUCKET_NAME`, `BUCKET_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: For S3/Backblaze storage.
    *   `MODEL_PATH`: Default `microsoft/VibeVoice-Realtime-0.5B`.
    *   `MODEL_DEVICE`: Default `cuda`.

## Current State & Files

*   **`Dockerfile`**: Installs system deps (including `ffmpeg`) and copies the bootstrap script.
*   **`runpod_bootstrap.sh`**: Handles venv creation, S3 cleanup, repo cloning, and dependency installation.
*   **`handler.py`**: The main inference entry point.
*   **`RP_SERVERLESS.md`**: The master plan and todo list.

## Project Context (VibeVoice)
*   **Purpose:** Long-form, multi-speaker TTS and real-time streaming.
*   **Tech Stack:** PyTorch, Hugging Face (Transformers, Diffusers), Flash Attention.
*   **Key Dependencies:** `torch==2.8.0` (in bootstrap), `sage_attn` (Flash Attention 2.8.3).

## Next Steps / Resume Instructions
1.  **Local Testing:** The user needs to verify the setup locally (simulating the RunPod environment).
2.  **Deployment:** Build the Docker image and deploy to RunPod.
3.  **Configuration:** Ensure all environment variables (especially S3 credentials) are set in the RunPod console.
4.  **Potential Future Work:** Investigate true dynamic reference audio conditioning if the preset-based approach is insufficient.
