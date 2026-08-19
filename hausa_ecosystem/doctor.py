import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


OPTIONAL_MODULES = {
    "flask": "Flask backend generator",
    "fastapi": "FastAPI backend generator",
    "uvicorn": "FastAPI server runner",
}


def run_doctor(args=None):
    checks = collect_doctor_checks()

    print("Hausa Ecosystem Doctor")
    print("=======================")
    for check in checks:
        icon = "PASS" if check["ok"] else "WARN"
        print(f"{icon}: {check['name']} - {check['message']}")

    warnings = sum(1 for check in checks if not check["ok"])
    print("-----------------------")
    print(f"Sakamako: {len(checks) - warnings} passed, {warnings} warnings")

    return 0


def collect_doctor_checks():
    checks = []
    checks.append(check_python_version())
    checks.append(check_command_available("hausa", "hausa CLI command is available", "Run: pip install -e ."))
    checks.append(check_command_available("rustc", "Rust compiler is available", "Install Rust if you want to run .hrust files"))
    checks.extend(check_optional_modules())
    checks.append(check_vscode_extension())
    checks.append(check_working_directory())
    return checks


def check_python_version():
    version = sys.version_info
    ok = version >= (3, 10)
    return {
        "name": "Python version",
        "ok": ok,
        "message": f"Python {platform.python_version()}" if ok else "Python 3.10+ is required",
    }


def check_command_available(command, success_message, failure_message):
    path = shutil.which(command)
    return {
        "name": f"Command: {command}",
        "ok": path is not None,
        "message": f"{success_message}: {path}" if path else failure_message,
    }


def check_optional_modules():
    checks = []
    for module_name, purpose in OPTIONAL_MODULES.items():
        installed = importlib.util.find_spec(module_name) is not None
        checks.append(
            {
                "name": f"Python module: {module_name}",
                "ok": installed,
                "message": purpose if installed else f"Optional. Install with: pip install {module_name}",
            }
        )
    return checks


def check_vscode_extension():
    extension_path = Path.home() / ".vscode" / "extensions" / "vscode-hausa"
    return {
        "name": "VS Code extension",
        "ok": extension_path.exists(),
        "message": f"Installed at {extension_path}" if extension_path.exists() else "Optional. Run: python install_extension.py",
    }


def check_working_directory():
    from core.database import user_data_directory

    data_dir = user_data_directory()
    parent = data_dir.parent
    return {
        "name": "User data directory",
        "ok": parent.exists() and os.access(parent, os.W_OK),
        "message": f"Optional vocabulary data: {data_dir}",
    }


def command_output(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=5)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as error:
        return 1, "", str(error)
