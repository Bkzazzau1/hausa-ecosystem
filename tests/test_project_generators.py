import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def run_package_cli(*args, cwd=ROOT_DIR):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    return subprocess.run(
        [sys.executable, "-m", "hausa_ecosystem.cli", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def test_generate_flask_backend_project(tmp_path):
    project_dir = tmp_path / "my_flask_api"

    result = run_package_cli("new", "backend", "flask", str(project_dir))

    assert result.returncode == 0
    assert (project_dir / "app.hausa").exists()
    assert (project_dir / "requirements.txt").read_text(encoding="utf-8") == "flask\n"
    assert "Injin_Yanar_Gizo" in (project_dir / "app.hausa").read_text(encoding="utf-8")
    assert "bude_rufa" in (project_dir / "app.hausa").read_text(encoding="utf-8")


def test_generate_fastapi_backend_project(tmp_path):
    project_dir = tmp_path / "my_fastapi_api"

    result = run_package_cli("new", "backend", "fastapi", str(project_dir))

    assert result.returncode == 0
    assert (project_dir / "app.hausa").exists()
    requirements = (project_dir / "requirements.txt").read_text(encoding="utf-8")
    assert "fastapi" in requirements
    assert "uvicorn" in requirements
    assert "Saurin_API" in (project_dir / "app.hausa").read_text(encoding="utf-8")


def test_generate_sqlite_database_project_and_run_it(tmp_path):
    project_dir = tmp_path / "my_db_app"

    result = run_package_cli("new", "database", "sqlite", str(project_dir))

    assert result.returncode == 0
    assert (project_dir / "app.hausa").exists()
    assert "bude_rufa" in (project_dir / "app.hausa").read_text(encoding="utf-8")

    run_result = run_package_cli("run", "app.hausa", cwd=project_dir)

    assert run_result.returncode == 0
    assert "Abu na farko" in run_result.stdout
    assert "Abu na biyu" in run_result.stdout
    assert (project_dir / "app.db").exists()


def test_project_generator_rejects_non_empty_folder(tmp_path):
    project_dir = tmp_path / "existing"
    project_dir.mkdir()
    (project_dir / "file.txt").write_text("already here", encoding="utf-8")

    result = run_package_cli("new", "backend", "flask", str(project_dir))

    assert result.returncode == 1
    assert "ba komai bane" in result.stdout
