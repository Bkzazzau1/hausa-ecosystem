from hausa_ecosystem import doctor


def test_check_python_version_passes_on_supported_python():
    result = doctor.check_python_version()

    assert result["name"] == "Python version"
    assert result["ok"] is True
    assert "Python" in result["message"]


def test_check_command_available_reports_missing_command(monkeypatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda command: None)

    result = doctor.check_command_available("missing-tool", "available", "install it")

    assert result["ok"] is False
    assert result["message"] == "install it"


def test_check_command_available_reports_existing_command(monkeypatch):
    monkeypatch.setattr(doctor.shutil, "which", lambda command: "TOOL_PATH")

    result = doctor.check_command_available("tool", "available", "install it")

    assert result["ok"] is True
    assert "TOOL_PATH" in result["message"]


def test_run_doctor_prints_summary(monkeypatch, capsys):
    monkeypatch.setattr(
        doctor,
        "collect_doctor_checks",
        lambda: [
            {"name": "One", "ok": True, "message": "fine"},
            {"name": "Two", "ok": False, "message": "optional missing"},
        ],
    )

    exit_code = doctor.run_doctor([])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Hausa Ecosystem Doctor" in captured.out
    assert "PASS: One" in captured.out
    assert "WARN: Two" in captured.out
    assert "Sakamako: 1 passed, 1 warnings" in captured.out


def test_check_working_directory_checks_user_data_parent(tmp_path, monkeypatch):
    monkeypatch.setenv("HAUSA_DATA_DIR", str(tmp_path / "hausa-data"))

    result = doctor.check_working_directory()

    assert result["ok"] is True
    assert "hausa-data" in result["message"]
