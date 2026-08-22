import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def run_package_cli(*args, cwd=ROOT_DIR):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(ROOT_DIR)
        if not existing_pythonpath
        else str(ROOT_DIR) + os.pathsep + existing_pythonpath
    )

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

    app_content = (project_dir / "app.hausa").read_text(encoding="utf-8")

    assert result.returncode == 0
    assert (project_dir / "app.hausa").exists()
    assert "flask>=3.0,<4" in (project_dir / "requirements.txt").read_text(encoding="utf-8")
    assert (project_dir / ".env.example").exists()
    assert (project_dir / "test_app.py").exists()
    assert "Injin_Yanar_Gizo" in app_content
    assert "bude_rufa" in app_content
    assert "methods=[\"POST\"]" in app_content
    assert "methods=[\"PUT\"]" in app_content
    assert "methods=[\"DELETE\"]" in app_content
    assert "sabunta_abu" in app_content
    assert "goge_abu" in app_content
    assert "debug=karya" in app_content


def test_generate_fastapi_backend_project(tmp_path):
    project_dir = tmp_path / "my_fastapi_api"

    result = run_package_cli("new", "backend", "fastapi", str(project_dir))

    app_content = (project_dir / "app.hausa").read_text(encoding="utf-8")
    requirements = (project_dir / "requirements.txt").read_text(encoding="utf-8")

    assert result.returncode == 0
    assert (project_dir / "app.hausa").exists()
    assert "fastapi" in requirements
    assert "uvicorn" in requirements
    assert "Saurin_API" in app_content
    assert "@app.aika" in app_content
    assert "@app.saka" in app_content
    assert "@app.goge_hanya" in app_content
    assert "sabunta_abu" in app_content
    assert "goge_abu" in app_content
    assert "sqlite3" in app_content
    assert (project_dir / ".env.example").exists()


def test_generate_django_backend_project_and_translate_view(tmp_path):
    project_dir = tmp_path / "my_django_site"

    result = run_package_cli("new", "backend", "django", str(project_dir))

    assert result.returncode == 0
    assert "hausa to-en main/views.hausa" in result.stdout
    assert "python manage.py runserver" in result.stdout
    assert (project_dir / "manage.py").exists()
    assert (project_dir / "config" / "settings.py").exists()
    assert (project_dir / "config" / "urls.py").exists()
    assert (project_dir / "main" / "views.hausa").exists()
    assert "django>=5.2,<7" in (project_dir / "requirements.txt").read_text(encoding="utf-8")
    assert "DJANGO_SECRET_KEY" in (project_dir / ".env.example").read_text(encoding="utf-8")

    translation = run_package_cli(
        "to-en", "main/views.hausa", "-o", "main/views.py", "--profile", "django", cwd=project_dir
    )
    translated = (project_dir / "main" / "views.py").read_text(encoding="utf-8")
    assert translation.returncode == 0
    assert "from django.http import JsonResponse" in translated
    assert "def shafi_na_farko(request):" in translated

    django_env = os.environ.copy()
    django_env["DJANGO_ALLOWED_HOSTS"] = "testserver"
    check = subprocess.run(
        [sys.executable, "manage.py", "check"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=django_env,
    )
    assert check.returncode == 0, check.stderr

    request = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import os; "
                "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); "
                "import django; django.setup(); "
                "from django.test import Client; "
                "response = Client().get('/'); "
                "assert response.status_code == 200; "
                "assert response.json()['sako'] == 'Sannu daga Hausa Django!'"
            ),
        ],
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=django_env,
    )
    assert request.returncode == 0, request.stderr


def test_generate_sqlite_database_project_and_run_it(tmp_path):
    project_dir = tmp_path / "my_db_app"

    result = run_package_cli("new", "database", "sqlite", str(project_dir))

    app_content = (project_dir / "app.hausa").read_text(encoding="utf-8")

    assert result.returncode == 0
    assert (project_dir / "app.hausa").exists()
    assert "bude_rufa" in app_content
    assert "kirkiri_abu" in app_content
    assert "samu_abu" in app_content
    assert "sabunta_abu" in app_content
    assert "goge_abu" in app_content

    run_result = run_package_cli("run", "app.hausa", cwd=project_dir)

    assert run_result.returncode == 0
    assert "Bayan kirkira" in run_result.stdout
    assert "Abu na farko" in run_result.stdout
    assert "Abu na biyu" in run_result.stdout
    assert "Bayan sabuntawa da gogewa" in run_result.stdout
    assert "Abu na farko da aka sabunta" in run_result.stdout
    assert (project_dir / "app.db").exists()


def test_project_generator_rejects_non_empty_folder(tmp_path):
    project_dir = tmp_path / "existing"
    project_dir.mkdir()
    (project_dir / "file.txt").write_text("already here", encoding="utf-8")

    result = run_package_cli("new", "backend", "flask", str(project_dir))

    assert result.returncode == 1
    assert "ba komai bane" in result.stdout
