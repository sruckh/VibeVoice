# Code Style and Conventions

While explicit configuration files for linting and formatting (e.g., `.flake8`, `pyproject.toml` with `black` or `isort` configs) were not found, the existing code in `demo/web/app.py` and `demo/vibevoice_realtime_demo.py` suggests the following conventions:

*   **Language**: Python 3.9+
*   **Imports**: Generally grouped: standard library, then third-party libraries, then local project modules.
*   **Type Hinting**: Used consistently for function parameters and return values (`Optional`, `Callable`, `Dict`, `Iterator`, `Tuple`, `Any`).
*   **Variable Naming**: `snake_case` for variables and functions.
*   **Class Naming**: `CamelCase` for classes.
*   **Constants**: Uppercase with underscores (`SAMPLE_RATE`, `BASE`).
*   **Environment Variables**: Used for configuration (`MODEL_PATH`, `MODEL_DEVICE`, `VOICE_PRESET`).
*   **Path Manipulation**: `pathlib.Path` is used for robust path handling.
*   **Logging**: `print()` statements are used for debugging and status updates during startup and runtime.
*   **Error Handling**: `try...except` blocks are used for handling exceptions, often with `traceback.print_exc()` for diagnostic logging.

## Suggested Tools for Enforcement:

To maintain and enforce code quality, it is recommended to integrate the following tools:

*   **Black**: An uncompromising code formatter.
*   **isort**: A utility to sort imports alphabetically and automatically separate them into sections.
*   **flake8**: A wrapper around PyFlakes, pycodestyle, and McCabe to check for Python style guide violations and programming errors.

These tools can be integrated into a `pre-commit` hook or CI/CD pipeline.