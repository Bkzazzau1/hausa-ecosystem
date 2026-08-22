from hausa_ecosystem import scan_cli


def test_find_hausa_files_returns_supported_files(tmp_path):
    good_file = tmp_path / "app.hausa"
    rust_file = tmp_path / "main.hrust"
    ignored_file = tmp_path / "notes.txt"

    good_file.write_text("buga('hi')", encoding="utf-8")
    rust_file.write_text("jama'a aiki main() {}", encoding="utf-8")
    ignored_file.write_text("hello", encoding="utf-8")

    files = scan_cli.find_hausa_files(tmp_path)

    assert good_file in files
    assert rust_file in files
    assert ignored_file not in files


def test_scan_project_passes_valid_hausa_file(tmp_path, capsys):
    source_file = tmp_path / "valid.hausa"
    source_file.write_text(
        '''
suna = "Bashir"
buga("Sannu", suna)
''',
        encoding="utf-8",
    )

    exit_code = scan_cli.scan_project(tmp_path)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Sakamako: 1 passed, 0 failed" in captured.out


def test_scan_project_warns_when_no_files_exist(tmp_path, capsys):
    exit_code = scan_cli.scan_project(tmp_path)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "WARN" in captured.out


def test_scan_project_fails_when_file_has_syntax_error(tmp_path, capsys):
    source_file = tmp_path / "invalid.hausa"
    source_file.write_text(
        '''
idan gaskiya
    buga("Missing colon")
''',
        encoding="utf-8",
    )

    exit_code = scan_cli.scan_project(tmp_path)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "failed" in captured.out
