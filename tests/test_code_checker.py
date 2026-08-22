import shutil

import pytest

from hausa_ecosystem.code_checker import check_hausa_python, check_hausa_rust, run_check_command


def test_check_hausa_python_passes_valid_file(tmp_path, capsys):
    source_file = tmp_path / "valid.hausa"
    source_file.write_text(
        '''
suna = "Bashir"
buga("Sannu", suna)
idan gaskiya:
    buga("Yana aiki")
''',
        encoding="utf-8",
    )

    exit_code = check_hausa_python(source_file)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "PASS" in captured.out


def test_check_hausa_python_fails_invalid_syntax(tmp_path, capsys):
    source_file = tmp_path / "invalid.hausa"
    source_file.write_text(
        '''
idan gaskiya
    buga("Missing colon")
''',
        encoding="utf-8",
    )

    exit_code = check_hausa_python(source_file)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "FAIL" in captured.out


def test_run_check_command_rejects_missing_file(capsys):
    exit_code = run_check_command(["missing.hausa"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Ba a sami fayil" in captured.out


def test_run_check_command_rejects_unknown_extension(tmp_path, capsys):
    source_file = tmp_path / "notes.txt"
    source_file.write_text("hello", encoding="utf-8")

    exit_code = run_check_command([str(source_file)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert ".hausa" in captured.out


@pytest.mark.skipif(shutil.which("rustc") is None, reason="rustc is not installed")
def test_check_hausa_rust_passes_valid_file(tmp_path, capsys):
    source_file = tmp_path / "valid.hrust"
    source_file.write_text(
        '''
jama'a aiki main() {
    bari sako = "Sannu";
    println!("{}", sako);
}
''',
        encoding="utf-8",
    )

    exit_code = check_hausa_rust(source_file)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "PASS" in captured.out
