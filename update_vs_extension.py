# update_vs_extension.py
import json
import os
import re

from core.database import load_dictionary_from_db
from core.dictionary import (
    PYTHON_BUILTIN_WORDS,
    PYTHON_CORE_WORDS,
    PYTHON_DATABASE_WORDS,
    PYTHON_VOCABULARY_PROFILES,
    PYTHON_WEB_WORDS,
    RUST_VOCABULARY_PROFILES,
)

PYTHON_KEYWORDS, RUST_KEYWORDS, _ = load_dictionary_from_db()

HAUSA_SYNTAX_PATH = "extensions/vscode-hausa/syntaxes/hausa.tmLanguage.json"
HRUST_SYNTAX_PATH = "extensions/vscode-hausa/syntaxes/hrust.tmLanguage.json"
VOCABULARY_PATH = "extensions/vscode-hausa/vocabularies.json"


def keyword_pattern(keywords):
    escaped = [re.escape(key) for key in sorted(keywords, key=lambda item: (-len(item), item))]
    # Word boundaries fail for valid Hausa words ending in apostrophes, such as
    # the Rust visibility keyword ``jama'a``.
    return "(?<![\\w'])(?:" + "|".join(escaped) + ")(?![\\w'])"


def python_syntax_patterns():
    constants = {key for key, value in PYTHON_KEYWORDS.items() if value in {"True", "False", "None"}}
    types = {
        key for key, value in PYTHON_KEYWORDS.items()
        if value in {"bool", "bytearray", "bytes", "complex", "dict", "float", "frozenset", "int", "list", "memoryview", "object", "set", "str", "tuple", "type"}
    }
    builtins = set(PYTHON_BUILTIN_WORDS) - constants - types
    frameworks = (set(PYTHON_DATABASE_WORDS) | set(PYTHON_WEB_WORDS)) - builtins - types
    control = set(PYTHON_CORE_WORDS) - constants - types - builtins
    return [
        {"name": "constant.language.hausa", "match": keyword_pattern(constants)},
        {"name": "storage.type.hausa", "match": keyword_pattern(types)},
        {"name": "support.function.builtin.hausa", "match": keyword_pattern(builtins)},
        {"name": "support.function.framework.hausa", "match": keyword_pattern(frameworks)},
        {"name": "keyword.control.hausa", "match": keyword_pattern(control)},
        {"include": "source.python"},
    ]


def rust_syntax_patterns():
    constants = {key for key, value in RUST_KEYWORDS.items() if value in {"true", "false"}}
    declarations = {
        key for key, value in RUST_KEYWORDS.items()
        if value in {"crate", "dyn", "enum", "extern", "impl", "mod", "pub", "ref", "Self", "self", "static", "struct", "super", "trait", "type", "unsafe", "use"}
    }
    control = set(RUST_KEYWORDS) - constants - declarations
    return [
        {"name": "constant.language.hrust", "match": keyword_pattern(constants)},
        {"name": "storage.modifier.hrust", "match": keyword_pattern(declarations)},
        {"name": "keyword.control.hrust", "match": keyword_pattern(control)},
        {"include": "source.rust"},
    ]


def vocabulary_metadata():
    python_constants = {key for key, value in PYTHON_KEYWORDS.items() if value in {"True", "False", "None"}}
    python_types = {
        key for key, value in PYTHON_KEYWORDS.items()
        if value in {"bool", "bytearray", "bytes", "complex", "dict", "float", "frozenset", "int", "list", "memoryview", "object", "set", "str", "tuple", "type"}
    }
    python_frameworks = set(PYTHON_DATABASE_WORDS) | set(PYTHON_WEB_WORDS)
    rust_constants = {key for key, value in RUST_KEYWORDS.items() if value in {"true", "false"}}
    rust_declarations = {
        key for key, value in RUST_KEYWORDS.items()
        if value in {"crate", "dyn", "enum", "extern", "impl", "mod", "pub", "ref", "Self", "self", "static", "struct", "super", "trait", "type", "unsafe", "use"}
    }

    python = {}
    for word, english in sorted(PYTHON_KEYWORDS.items()):
        if word in python_constants:
            category = "constant"
        elif word in python_types:
            category = "type"
        elif word in python_frameworks:
            category = "framework"
        elif word in PYTHON_BUILTIN_WORDS:
            category = "builtin"
        else:
            category = "keyword"
        python[word] = {
            "english": english,
            "category": category,
            "profiles": sorted(name for name, mapping in PYTHON_VOCABULARY_PROFILES.items() if word in mapping),
        }

    rust = {}
    for word, english in sorted(RUST_KEYWORDS.items()):
        category = "constant" if word in rust_constants else "declaration" if word in rust_declarations else "keyword"
        rust[word] = {
            "english": english,
            "category": category,
            "profiles": sorted(name for name, mapping in RUST_VOCABULARY_PROFILES.items() if word in mapping),
        }
    return {"python": python, "rust": rust}


def update_syntax_files():
    # 1. Update Hausa Python Syntax Highlighting
    if os.path.exists(HAUSA_SYNTAX_PATH):
        with open(HAUSA_SYNTAX_PATH, 'r', encoding='utf-8') as f:
            hausa_data = json.load(f)

        hausa_data["patterns"] = python_syntax_patterns()

        with open(HAUSA_SYNTAX_PATH, 'w', encoding='utf-8') as f:
            json.dump(hausa_data, f, indent=2, ensure_ascii=False)
        print("Hausa Python syntax highlighter maps updated smoothly!")

    # 2. Update Hausa Rust Syntax Highlighting
    if os.path.exists(HRUST_SYNTAX_PATH):
        with open(HRUST_SYNTAX_PATH, 'r', encoding='utf-8') as f:
            hrust_data = json.load(f)

        hrust_data["patterns"] = rust_syntax_patterns()

        with open(HRUST_SYNTAX_PATH, 'w', encoding='utf-8') as f:
            json.dump(hrust_data, f, indent=2, ensure_ascii=False)
        print("Hausa Rust syntax highlighter maps updated smoothly!")

    vocabulary_path = os.path.dirname(VOCABULARY_PATH)
    os.makedirs(vocabulary_path, exist_ok=True)
    with open(VOCABULARY_PATH, "w", encoding="utf-8") as f:
        json.dump(vocabulary_metadata(), f, indent=2, ensure_ascii=False)
    print("VS Code completion and hover vocabulary updated smoothly!")


if __name__ == "__main__":
    update_syntax_files()
