import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXTENSION_DIR = ROOT_DIR / "extensions" / "vscode-hausa"


def test_vscode_extension_registers_snippets():
    package_json = json.loads((EXTENSION_DIR / "package.json").read_text(encoding="utf-8"))

    snippets = package_json["contributes"]["snippets"]

    assert {item["language"] for item in snippets} == {"hausa", "hrust"}
    assert any(item["path"] == "./snippets/hausa.code-snippets" for item in snippets)
    assert any(item["path"] == "./snippets/hrust.code-snippets" for item in snippets)


def test_hausa_snippets_are_valid_json_and_include_backend_shortcuts():
    snippets = json.loads((EXTENSION_DIR / "snippets" / "hausa.code-snippets").read_text(encoding="utf-8"))

    assert "Hausa Print" in snippets
    assert "SQLite Starter" in snippets
    assert "Flask Route" in snippets
    assert "FastAPI Route" in snippets
    assert snippets["Hausa Print"]["prefix"] == "buga"


def test_hrust_snippets_are_valid_json_and_include_rust_shortcuts():
    snippets = json.loads((EXTENSION_DIR / "snippets" / "hrust.code-snippets").read_text(encoding="utf-8"))

    assert "Hausa Rust Main" in snippets
    assert "Hausa Rust Let" in snippets
    assert "Hausa Rust If" in snippets
    assert snippets["Hausa Rust Main"]["prefix"] == "main"
