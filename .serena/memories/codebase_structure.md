# Codebase Structure

The VibeVoice project has a clear and modular structure, organized to separate core logic from demos and documentation.

```
/opt/docker/VibeVoice/
├───.git/                    # Git version control system directory
├───.serena/                 # Serena-specific configuration and memories
├───demo/                    # Demonstrations and examples of VibeVoice in action
│   ├───realtime_model_inference_from_file.py  # Script for real-time inference from file
│   ├───vibevoice_realtime_colab.ipynb         # Colab notebook for real-time demo
│   ├───vibevoice_realtime_demo.py             # Wrapper script to run the web demo
│   ├───text_examples/       # Example text inputs
│   ├───voices/              # Pre-trained voice presets
│   │   └───streaming_model/ # Specific voice models for streaming
│   │       ├───en-Carter_man.pt
│   │       └───... (other .pt voice files)
│   └───web/                 # Web-based real-time demo
│       ├───app.py           # FastAPI application for streaming TTS
│       └───index.html       # Frontend HTML for the web demo
├───docs/                    # Project documentation
│   └───vibevoice-realtime-0.5b.md # Documentation for the real-time model
├───Figures/                 # Images and figures used in documentation and README
├───vibevoice/               # Core VibeVoice source code
│   ├───__init__.py          # Python package initializer
│   ├───configs/             # Configuration files for different model variants
│   │   ├───qwen2.5_1.5b_64k.json
│   │   └───qwen2.5_7b_32k.json
│   ├───modular/             # Modular components of the VibeVoice model
│   │   ├───__init__.py
│   │   ├───configuration_vibevoice_streaming.py # Model configuration for streaming
│   │   ├───configuration_vibevoice.py           # General model configuration
│   │   ├───modeling_vibevoice_streaming_inference.py # Streaming inference model
│   │   ├───modeling_vibevoice_streaming.py      # Streaming model definition
│   │   ├───modular_vibevoice_diffusion_head.py  # Diffusion head component
│   │   ├───modular_vibevoice_text_tokenizer.py  # Text tokenizer component
│   │   ├───modular_vibevoice_tokenizer.py       # General tokenizer component
│   │   └───streamer.py                          # Audio streamer utility
│   ├───processor/           # Text and audio processing components
│   │   ├───__init__.py
│   │   ├───vibevoice_processor.py               # General VibeVoice processor
│   │   ├───vibevoice_streaming_processor.py     # Streaming specific processor
│   │   └───vibevoice_tokenizer_processor.py     # Tokenizer processor
│   ├───schedule/            # Scheduling-related algorithms
│   │   ├───__init__.py
│   │   ├───dpm_solver.py                        # DPM-Solver implementation
│   │   └───timestep_sampler.py                  # Timestep sampler
│   └───scripts/             # Utility scripts
│       ├───__init__.py
│       └───convert_nnscaler_checkpoint_to_transformers.py # Checkpoint conversion
├───.gitignore               # Git ignore file
├───CLAUDE.md                # (Potentially related to another AI model or documentation)
├───LICENSE                  # Project license information
├───pyproject.toml           # Project metadata and dependencies (PEP 621)
├───README.md                # Project overview and main documentation
└───SECURITY.md              # Security guidelines and policies
```

## Key Observations:

*   **Core Logic (`vibevoice/`):** Contains the actual implementation of the VibeVoice models, including configurations, modular components (streaming, diffusion, tokenizers), processors, and scheduling algorithms.
*   **Demos (`demo/`):** Provides various ways to interact with the models, from Python scripts to a full web-based streaming application and a Colab notebook. This clearly separates usage examples from the core library.
*   **Documentation (`docs/`, `README.md`):** Comprehensive information about the project, its capabilities, and technical details.
*   **Dependencies (`pyproject.toml`):** Modern Python project management for dependencies.
*   **Assets (`Figures/`, `demo/voices/`):** Dedicated directories for visual and audio assets.