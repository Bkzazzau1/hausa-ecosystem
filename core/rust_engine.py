# core/rust_engine.py
import os
import re
import subprocess
import sys
from pathlib import Path

from core.database import load_dictionary_from_db

_, RUST_KEYWORDS, RUST_ERRORS = load_dictionary_from_db()

# Create the reverse map dynamically for English-to-Hausa translation.
REVERSE_RUST_KEYWORDS = {v: k for k, v in RUST_KEYWORDS.items()}


def translate_logic(text, mapping):
    """Translate Rust identifiers without touching strings or comments."""
    output = []
    index = 0
    length = len(text)

    while index < length:
        char = text[index]
        next_char = text[index + 1] if index + 1 < length else ""

        if char == '"':
            segment, index = consume_quoted_string(text, index, '"')
            output.append(segment)
            continue

        if char == "'":
            segment, index = consume_quoted_string(text, index, "'")
            output.append(segment)
            continue

        if char == "/" and next_char == "/":
            segment, index = consume_line_comment(text, index)
            output.append(segment)
            continue

        if char == "/" and next_char == "*":
            segment, index = consume_block_comment(text, index)
            output.append(segment)
            continue

        if is_identifier_start(char):
            identifier, index = consume_identifier(text, index)
            output.append(mapping.get(identifier, identifier))
            continue

        output.append(char)
        index += 1

    return "".join(output)


def is_identifier_start(char):
    return char == "_" or char == "'" or char.isalpha()


def is_identifier_part(char):
    return char == "_" or char == "'" or char.isalnum()


def consume_identifier(text, start):
    index = start
    while index < len(text) and is_identifier_part(text[index]):
        index += 1
    return text[start:index], index


def consume_quoted_string(text, start, quote):
    index = start + 1
    escaped = False

    while index < len(text):
        char = text[index]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            index += 1
            break
        index += 1

    return text[start:index], index


def consume_line_comment(text, start):
    index = text.find("\n", start)
    if index == -1:
        return text[start:], len(text)
    return text[start:index], index


def consume_block_comment(text, start):
    index = text.find("*/", start + 2)
    if index == -1:
        return text[start:], len(text)
    return text[start:index + 2], index + 2


def hrust_to_english(hrust_code):
    return translate_logic(hrust_code, RUST_KEYWORDS)


def english_to_hrust(english_code):
    return translate_logic(english_code, REVERSE_RUST_KEYWORDS)


def translate_source(source):
    return hrust_to_english(source)


def translate_file(filepath):
    return translate_source(Path(filepath).read_text(encoding='utf-8'))


def write_translated_file(filepath, output=None):
    source_path = Path(filepath)
    output_path = Path(output) if output else source_path.with_suffix(".rs")
    output_path.write_text(translate_file(source_path), encoding="utf-8")
    return output_path


def run_file(filepath):
    return run_rust_code(filepath)


def run_rust_code(filepath):
    """Translates a .hrust file to standard Rust, compiles it, runs it, and cleans up."""
    source_path = Path(filepath)
    if not source_path.exists():
        print(f"Kuskure: Ba a sami fayil din ba a: {filepath}")
        return 1

    hrust_source = source_path.read_text(encoding='utf-8')

    # Step 1: Translate Hausa-Rust to standard Rust.
    english_source = hrust_to_english(hrust_source)

    # Step 2: Create temporary compiler outputs beside the source file.
    base_name = source_path.with_suffix("")
    rs_filepath = base_name.with_name(base_name.name + "_temp.rs")
    exe_suffix = ".exe" if sys.platform == "win32" else ""
    exe_filepath = base_name.with_name(base_name.name + f"_temp{exe_suffix}")
    pdb_filepath = exe_filepath.with_suffix(".pdb")

    rs_filepath.write_text(english_source, encoding='utf-8')

    try:
        # Step 3: Run the native Rust compiler.
        compile_process = subprocess.run(
            ["rustc", str(rs_filepath), "-o", str(exe_filepath)],
            capture_output=True,
            text=True,
        )

        if compile_process.returncode != 0:
            translated_error = localize_rust_errors(compile_process.stderr)

            print("\n" + "=" * 60)
            print("AN SAMI KUSKUREN RUSTC YAYIN HADASWA (Compilation Error):")
            print(translated_error, end="")
            print("=" * 60 + "\n")
            return compile_process.returncode

        # Step 4: Run the generated executable binary file.
        run_process = subprocess.run(
            [str(exe_filepath.resolve())],
            capture_output=True,
            text=True,
        )

        if run_process.stdout:
            print(run_process.stdout, end="")
        if run_process.stderr:
            print(run_process.stderr, end="", file=sys.stderr)
        return run_process.returncode

    except FileNotFoundError:
        print("\n" + "=" * 50)
        print("KUSKURE: Ba a sami 'rustc' ba a kan kwamfutarka!")
        print("Tabbatar ka girka Rust (Rustup) sannan ka saka shi a cikin PATH dinka.")
        print("=" * 50 + "\n")
        return 1

    finally:
        # Step 5: Clean up temporary files so the workspace stays clean.
        for temp_path in (rs_filepath, exe_filepath, pdb_filepath):
            if temp_path.exists():
                os.remove(temp_path)


def localize_rust_errors(error_text):
    """Translate known rustc message fragments into Hausa explanations."""
    translated = error_text
    for english, hausa in RUST_ERRORS.items():
        translated = re.sub(re.escape(english), hausa, translated, flags=re.IGNORECASE)
    return translated
