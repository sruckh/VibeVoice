FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/workspace/VibeVoice/cache \
    HUGGINGFACE_HUB_CACHE=/workspace/VibeVoice/cache \
    WORKSPACE=/workspace/VibeVoice

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3.12-dev python3-pip \
    git ca-certificates curl build-essential cmake ninja-build pkg-config ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.12 /usr/local/bin/python \
    && ln -sf /usr/bin/pip3 /usr/local/bin/pip

WORKDIR /workspace/VibeVoice

# At this point, only the bootstrap script will be copied into the container.
# The VibeVoice repository will be cloned by the bootstrap script at runtime.
COPY runpod_bootstrap.sh /workspace/VibeVoice/runpod_bootstrap.sh

CMD ["bash", "/workspace/VibeVoice/runpod_bootstrap.sh"]

