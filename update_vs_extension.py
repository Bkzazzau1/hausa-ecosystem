# update_vs_extension.py
import json
import os
import re

from core.database import load_dictionary_from_db

PYTHON_KEYWORDS, RUST_KEYWORDS, _ = load_dictionary_from_db()

HAUSA_SYNTAX_PATH = "extensions/vscode-hausa/syntaxes/hausa.tmLanguage.json"
HRUST_SYNTAX_PATH = "extensions/vscode-hausa/syntaxes/hrust.tmLanguage.json"


def keyword_pattern(keywords):
    escaped = [re.escape(key) for key in keywords]
    return "\\b(" + "|".join(escaped) + ")\\b"


def update_syntax_files():
    # 1. Update Hausa Python Syntax Highlighting
    if os.path.exists(HAUSA_SYNTAX_PATH):
        with open(HAUSA_SYNTAX_PATH, 'r', encoding='utf-8') as f:
            hausa_data = json.load(f)

        hausa_data["patterns"] = [
            {"name": "comment.line.number-sign.hausa", "match": "#.*$"},
            {"name": "string.quoted.double.hausa", "begin": "\"", "end": "\""},
            {"name": "string.quoted.single.hausa", "begin": "'", "end": "'"},
            {"name": "keyword.control.hausa", "match": keyword_pattern(PYTHON_KEYWORDS.keys())},
        ]

        with open(HAUSA_SYNTAX_PATH, 'w', encoding='utf-8') as f:
            json.dump(hausa_data, f, indent=2, ensure_ascii=False)
        print("Hausa Python syntax highlighter maps updated smoothly!")

    # 2. Update Hausa Rust Syntax Highlighting
    if os.path.exists(HRUST_SYNTAX_PATH):
        with open(HRUST_SYNTAX_PATH, 'r', encoding='utf-8') as f:
            hrust_data = json.load(f)

        hrust_data["patterns"] = [
            {"name": "comment.line.double-slash.hrust", "match": "//.*$"},
            {"name": "string.quoted.double.hrust", "begin": "\"", "end": "\""},
            {"name": "keyword.control.hrust", "match": keyword_pattern(RUST_KEYWORDS.keys())},
        ]

        with open(HRUST_SYNTAX_PATH, 'w', encoding='utf-8') as f:
            json.dump(hrust_data, f, indent=2, ensure_ascii=False)
        print("Hausa Rust syntax highlighter maps updated smoothly!")


if __name__ == "__main__":
    update_syntax_files()
