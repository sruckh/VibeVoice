# Suggested Commands for VibeVoice Development

This document outlines key commands for setting up, running, and developing within the VibeVoice project.

## 1. Project Setup and Dependencies

### Install Python Dependencies
The project uses `setuptools` for packaging and `pyproject.toml` to manage dependencies.
To install all required libraries:
```bash
pip install .
```
Or, if you prefer to install in editable mode for development:
```bash
pip install -e .
```

## 2. Running Demos

### 2.1. Real-time Streaming Web Demo (FastAPI/Uvicorn)

The primary real-time demo is a web application accessible via a browser.

**Required Environment Variables:**
*   `MODEL_PATH`: Path to the VibeVoice model (e.g., a directory containing `config.json` and model weights). This is crucial.
*   `MODEL_DEVICE`: (Optional) Specifies the device for model inference (`cuda`, `cpu`, `mpx`, `mps`). Defaults to `cuda`.
*   `VOICE_PRESET`: (Optional) Specifies a default voice preset to use.

**To run the web demo:**
Navigate to the project root and execute the wrapper script:
```bash
python demo/vibevoice_realtime_demo.py --model_path /path/to/your/model --port 8000 --device cuda
```
Replace `/path/to/your/model` with the actual path to your VibeVoice model.
Access the demo in your browser at `http://localhost:8000` (or your specified port).

**Example without the wrapper script (if environment variables are set directly):**
```bash
export MODEL_PATH="/path/to/your/model"
export MODEL_DEVICE="cuda"
uvicorn demo.web.app:app --host 0.0.0.0 --port 8000 --reload
```

### 2.2. Colab Notebook Demo
A Colab notebook is provided for interactive demonstration.
*   **Access:** `demo/vibevoice_realtime_colab.ipynb`
*   **Direct Link (from README):** `https://colab.research.google.com/github/microsoft/VibeVoice/blob/main/demo/vibevoice_realtime_colab.ipynb`

## 3. Code Quality and Maintenance (Suggested)

While no explicit configurations were found, it is recommended to use the following tools for code quality:

*   **Formatting**:
    *   `black .`: Automatically formats Python code.
    *   `isort .`: Sorts and formats Python imports.
*   **Linting**:
    *   `flake8 .`: Checks for style guide violations and programming errors.

## 4. General System Commands

*   `git status`: Check the status of your Git repository.
*   `git add .`: Stage all changes for commit.
*   `git commit -m "Your commit message"`: Commit staged changes.
*   `ls -F`: List files and directories in the current directory.
*   `cd <directory>`: Change directory.
*   `grep -r "pattern" .`: Search for a pattern recursively in the current directory.
*   `find . -name "*.py"`: Find Python files in the current directory.

## 5. What to do when a task is completed

After making changes or implementing a new feature, follow these steps:
1.  Run all relevant formatting and linting checks (e.g., `black`, `isort`, `flake8`).
2.  Ensure all demos or entry points still function as expected.
3.  If new functionality is added, consider adding unit tests if a testing framework is introduced.
4.  Commit your changes with a clear and concise message.