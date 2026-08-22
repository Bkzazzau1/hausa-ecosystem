# Doctor Command

Use the doctor command to check whether your Hausa Ecosystem development environment is ready.

```bash
hausa doctor
```

It checks:

```text
Python version
hausa command availability
Rust compiler availability
Flask module
FastAPI module
Uvicorn module
VS Code extension installation
Project root files
```

Warnings do not always mean the project is broken. Some tools are optional:

- Rust is only required for `.hrust` files.
- Flask is only required for Flask backend projects.
- FastAPI and Uvicorn are only required for FastAPI backend projects.
- VS Code extension is only required for editor highlighting.

A healthy setup should show mostly `PASS` results.
