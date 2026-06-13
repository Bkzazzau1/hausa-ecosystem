import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CLI = ROOT_DIR / "h-run.py"


def run_cli(*args, cwd=ROOT_DIR):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_version_command():
    result = run_cli("--version")

    assert result.returncode == 0
    assert "Hausa Ecosystem CLI" in result.stdout


def test_cli_keywords_command_lists_python_keywords():
    result = run_cli("keywords", "python")

    assert result.returncode == 0
    assert "buga -> print" in result.stdout
    assert "idan -> if" in result.stdout


def test_cli_new_python_creates_starter_file(tmp_path):
    output_file = tmp_path / "app.hausa"

    result = run_cli("new", "python", str(output_file))

    assert result.returncode == 0
    assert output_file.exists()
    assert "buga" in output_file.read_text(encoding="utf-8")
    assert "idan gaskiya" in output_file.read_text(encoding="utf-8")


def test_cli_new_rust_creates_starter_file(tmp_path):
    output_file = tmp_path / "app.hrust"

    result = run_cli("new", "rust", str(output_file))

    assert result.returncode == 0
    assert output_file.exists()
    assert "jama'a aiki main" in output_file.read_text(encoding="utf-8")
    assert "bari sauya" in output_file.read_text(encoding="utf-8")


def test_cli_to_en_writes_translation_to_output_file(tmp_path):
    source_file = tmp_path / "hello.hausa"
    output_file = tmp_path / "hello.py"
    source_file.write_text(
        '''
suna = "Bashir"
buga("Sannu", suna)
idan gaskiya:
    buga("Yana aiki")
''',
        encoding="utf-8",
    )

    result = run_cli("to-en", str(source_file), "-o", str(output_file))

    assert result.returncode == 0
    assert output_file.exists()
    translated = output_file.read_text(encoding="utf-8")
    assert 'print("Sannu", suna)' in translated
    assert "if True:" in translated


def test_cli_to_ha_writes_translation_to_output_file(tmp_path):
    source_file = tmp_path / "hello.py"
    output_file = tmp_path / "hello.hausa"
    source_file.write_text(
        '''
name = "Bashir"
print("Hello", name)
if True:
    print("It works")
''',
        encoding="utf-8",
    )

    result = run_cli("to-ha", str(source_file), "-o", str(output_file))

    assert result.returncode == 0
    assert output_file.exists()
    translated = output_file.read_text(encoding="utf-8")
    assert 'buga("Hello", name)' in translated
    assert "idan gaskiya:" in translated
