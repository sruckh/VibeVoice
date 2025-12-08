# Tech Stack

The VibeVoice project is primarily built using **Python (>=3.9)** and leverages a variety of libraries common in the machine learning and web development ecosystems.

## Core Libraries:
*   **PyTorch**: The foundational deep learning framework.
*   **Hugging Face Ecosystem**:
    *   `accelerate==1.6.0`: For distributed training and inference.
    *   `transformers==4.51.3`: For working with pre-trained models, specifically `VibeVoiceStreamingForConditionalGenerationInference` and `VibeVoiceStreamingProcessor`.
    *   `diffusers`: For diffusion models, central to VibeVoice's architecture.
*   **Performance Optimization**:
    *   `llvmlite>=0.40.0`
    *   `numba>=0.57.0`: Likely used for JIT compilation to optimize Python code performance.
*   **Scientific Computing & Data Processing**:
    *   `tqdm`: For progress bars.
    *   `numpy`: Fundamental package for numerical computation.
    *   `scipy`: Scientific computing library.
    *   `librosa`: For audio analysis.
    *   `ml-collections`, `absl-py`: Utility libraries, potentially for configuration management.

## Web/Demo Related Libraries:
*   **FastAPI**: Modern, fast web framework for building APIs, used for the real-time streaming demo.
*   **uvicorn[standard]**: ASGI server, used to run FastAPI applications.
*   **gradio**: For building interactive web demos, often used in ML projects for quick prototyping and visualization.
*   **av**: Pythonic bindings for FFmpeg, likely used for audio processing/streaming.
*   **aiortc**: WebRTC for Python, likely for real-time communication aspects.

## Other:
*   `setuptools`: For package building and distribution.
*   `pathlib`: For object-oriented filesystem paths.