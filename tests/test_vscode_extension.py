import json
import shutil
import struct
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXTENSION_DIR = ROOT_DIR / "extensions" / "vscode-hausa"


def test_vscode_extension_registers_snippets():
    package_json = json.loads((EXTENSION_DIR / "package.json").read_text(encoding="utf-8"))

    snippets = package_json["contributes"]["snippets"]

    assert {item["language"] for item in snippets} == {"hausa", "hrust"}
    assert any(item["path"] == "./snippets/hausa.code-snippets" for item in snippets)
    assert any(item["path"] == "./snippets/hrust.code-snippets" for item in snippets)
    languages = {item["id"]: item for item in package_json["contributes"]["languages"]}
    assert languages["hausa"]["configuration"] == "./language-configuration-hausa.json"
    assert languages["hrust"]["configuration"] == "./language-configuration-hrust.json"


def test_vscode_extension_marketplace_metadata_and_docs_exist():
    package_json = json.loads((EXTENSION_DIR / "package.json").read_text(encoding="utf-8"))
    assert package_json["publisher"] == "hausaecosystem"
    assert package_json["version"] == "1.3.0"
    assert package_json["icon"] == "images/icon.png"
    assert package_json["license"] == "SEE LICENSE IN LICENSE"
    assert package_json["repository"]["url"].startswith("https://github.com/")
    assert set(package_json["categories"]) >= {"Programming Languages", "Snippets", "Education"}
    for filename in ("README.md", "CHANGELOG.md", "SUPPORT.md", "LICENSE"):
        assert (EXTENSION_DIR / filename).is_file()


def test_marketplace_images_are_valid_png_files():
    expected_sizes = {
        "icon.png": (256, 256),
        "hausa-python-preview.png": (1100, 620),
        "hausa-rust-preview.png": (1100, 620),
    }
    for filename, expected_size in expected_sizes.items():
        image_path = EXTENSION_DIR / "images" / filename
        data = image_path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        assert struct.unpack(">II", data[16:24]) == expected_size


def test_language_configurations_use_correct_comments():
    hausa = json.loads((EXTENSION_DIR / "language-configuration-hausa.json").read_text(encoding="utf-8"))
    hrust = json.loads((EXTENSION_DIR / "language-configuration-hrust.json").read_text(encoding="utf-8"))
    assert hausa["comments"]["lineComment"] == "#"
    assert hrust["comments"]["lineComment"] == "//"
    assert hrust["comments"]["blockComment"] == ["/*", "*/"]
    assert "increaseIndentPattern" in hausa["indentationRules"]
    assert {tuple(pair) for pair in hausa["surroundingPairs"]} >= {("(", ")"), ("{", "}")}
    assert {tuple(pair) for pair in hrust["surroundingPairs"]} >= {("(", ")"), ("{", "}")}


def test_grammars_have_semantic_scopes_and_no_mojibake():
    hausa_text = (EXTENSION_DIR / "syntaxes" / "hausa.tmLanguage.json").read_text(encoding="utf-8")
    hrust_text = (EXTENSION_DIR / "syntaxes" / "hrust.tmLanguage.json").read_text(encoding="utf-8")
    hausa = json.loads(hausa_text)
    hrust = json.loads(hrust_text)
    hausa_scopes = {pattern.get("name") for pattern in hausa["patterns"]}
    hrust_scopes = {pattern.get("name") for pattern in hrust["patterns"]}
    assert "constant.language.hausa" in hausa_scopes
    assert "storage.type.hausa" in hausa_scopes
    assert "support.function.builtin.hausa" in hausa_scopes
    assert "support.function.framework.hausa" in hausa_scopes
    assert "storage.modifier.hrust" in hrust_scopes
    assert "buƙata" in hausa_text
    assert "buÆ™ata" not in hausa_text
    assert "jama'a" in hrust_text


def test_marketplace_readme_references_existing_preview_images_and_examples():
    readme = (EXTENSION_DIR / "README.md").read_text(encoding="utf-8")
    assert "images/hausa-python-preview.png" in readme
    assert "images/hausa-rust-preview.png" in readme
    assert "aiki gaisuwa" in readme
    assert "jama'a aiki main" in readme


def test_vscode_110_commands_settings_and_runtime_are_registered():
    package_json = json.loads((EXTENSION_DIR / "package.json").read_text(encoding="utf-8"))
    assert package_json["main"] == "./extension.js"
    commands = {item["command"] for item in package_json["contributes"]["commands"]}
    assert commands == {
        "hausa.runFile",
        "hausa.checkFile",
        "hausa.translateToEnglish",
        "hausa.translateToHausa",
        "hausa.selectProfile",
    }
    assert all(not item["title"].startswith("Hausa:") for item in package_json["contributes"]["commands"])
    properties = package_json["contributes"]["configuration"]["properties"]
    assert properties["hausa.executablePath"]["default"] == "hausa"
    assert properties["hausa.vocabularyProfile"]["default"] == "all"
    assert properties["hausa.diagnosticsOnSave"]["default"] is True
    assert (EXTENSION_DIR / "extension.js").is_file()


def test_vscode_120_live_diagnostics_and_profile_completions_are_registered():
    package_json = json.loads((EXTENSION_DIR / "package.json").read_text(encoding="utf-8"))
    properties = package_json["contributes"]["configuration"]["properties"]
    assert properties["hausa.diagnosticsOnType"]["default"] is False
    assert properties["hausa.diagnosticsDelayMs"]["default"] == 750
    assert properties["hausa.diagnosticsDelayMs"]["minimum"] >= 250

    runtime = (EXTENSION_DIR / "extension.js").read_text(encoding="utf-8")
    assert "onDidChangeTextDocument" in runtime
    assert "mkdtemp" in runtime
    assert "details.profiles.includes(profile)" in runtime
    assert "translator did not create" in runtime


def test_generated_completion_vocabulary_matches_runtime_dictionary():
    from core.database import load_dictionary_from_db

    python_keywords, rust_keywords, _ = load_dictionary_from_db()
    vocabulary = json.loads((EXTENSION_DIR / "vocabularies.json").read_text(encoding="utf-8"))
    assert {word: item["english"] for word, item in vocabulary["python"].items()} == python_keywords
    assert {word: item["english"] for word, item in vocabulary["rust"].items()} == rust_keywords
    assert vocabulary["python"]["buga"]["category"] == "builtin"
    assert vocabulary["python"]["gaskiya"]["category"] == "constant"
    assert vocabulary["rust"]["jama'a"]["category"] == "declaration"


def test_extension_javascript_has_valid_syntax():
    node = shutil.which("node")
    if node is None:
        return
    result = subprocess.run(
        [node, "--check", str(EXTENSION_DIR / "extension.js")],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr


def test_hausa_snippets_are_valid_json_and_include_backend_shortcuts():
    snippets = json.loads((EXTENSION_DIR / "snippets" / "hausa.code-snippets").read_text(encoding="utf-8"))

    assert "Hausa Print" in snippets
    assert "SQLite Starter" in snippets
    assert "Flask Route" in snippets
    assert "FastAPI Route" in snippets
    assert "Django JSON View" in snippets
    assert snippets["Hausa Print"]["prefix"] == "buga"
    assert snippets["Django JSON View"]["prefix"] == "django-view"


def test_hrust_snippets_are_valid_json_and_include_rust_shortcuts():
    snippets = json.loads((EXTENSION_DIR / "snippets" / "hrust.code-snippets").read_text(encoding="utf-8"))

    assert "Hausa Rust Main" in snippets
    assert "Hausa Rust Let" in snippets
    assert "Hausa Rust If" in snippets
    assert snippets["Hausa Rust Main"]["prefix"] == "main"
