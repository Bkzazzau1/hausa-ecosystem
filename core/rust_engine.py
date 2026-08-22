# core/rust_engine.py
import re
import subprocess
import sys
import tempfile
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

        raw = consume_raw_string(text, index)
        if raw is not None:
            segment, index = raw
            output.append(segment)
            continue

        if char == '"':
            segment, index = consume_quoted_string(text, index, '"')
            output.append(segment)
            continue

        if char == "'":
            char_literal = consume_rust_char(text, index)
            if char_literal is not None:
                segment, index = char_literal
                output.append(segment)
                continue
            # Lifetimes are names, not vocabulary (notably the built-in 'static).
            end = index + 1
            while end < length and is_identifier_part(text[end]):
                end += 1
            output.append(text[index:end])
            index = end
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
    return char == "_" or char.isalpha()


def is_identifier_part(char):
    # Hausa words can contain an apostrophe (for example ``jama'a``). A leading
    # apostrophe is handled separately as a Rust lifetime or character literal.
    return char in ("_", "'") or char.isalnum()


def consume_raw_string(text, start):
    """Consume Rust r/raw byte strings, returning None when not at one."""
    prefix = start
    if text.startswith("br", start):
        prefix += 2
    elif text.startswith("r", start):
        prefix += 1
    else:
        return None
    hashes = 0
    while prefix < len(text) and text[prefix] == "#":
        hashes += 1
        prefix += 1
    if prefix >= len(text) or text[prefix] != '"':
        return None
    terminator = '"' + "#" * hashes
    end = text.find(terminator, prefix + 1)
    end = len(text) if end == -1 else end + len(terminator)
    return text[start:end], end


def consume_rust_char(text, start):
    index = start + 1
    if index >= len(text):
        return None
    if text[index] == "\\":
        index += 2
    else:
        index += 1
    if index < len(text) and text[index] == "'":
        return text[start:index + 1], index + 1
    return None


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
    index = start + 2
    depth = 1
    while index < len(text) and depth:
        if text.startswith("/*", index):
            depth += 1
            index += 2
        elif text.startswith("*/", index):
            depth -= 1
            index += 2
        else:
            index += 1
    return text[start:index], index


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


def run_rust_code(filepath, timeout=30):
    """Translates a .hrust file to standard Rust, compiles it, runs it, and cleans up."""
    source_path = Path(filepath)
    if not source_path.exists():
        print(f"Kuskure: Ba a sami fayil din ba a: {filepath}")
        return 1

    try:
        hrust_source = source_path.read_text(encoding='utf-8')
    except (IsADirectoryError, PermissionError, UnicodeError) as error:
        print(f"Kuskure: Ba a iya karanta fayil din {filepath}: {error}")
        return 1

    # Step 1: Translate Hausa-Rust to standard Rust.
    english_source = hrust_to_english(hrust_source)

    try:
        with tempfile.TemporaryDirectory(prefix="hausa-rust-") as temp_dir:
            rs_filepath = Path(temp_dir) / source_path.with_suffix(".rs").name
            exe_suffix = ".exe" if sys.platform == "win32" else ""
            exe_filepath = Path(temp_dir) / f"hausa_program{exe_suffix}"
            rs_filepath.write_text(english_source, encoding='utf-8')
            compile_process = subprocess.run(
                ["rustc", str(rs_filepath), "-o", str(exe_filepath)],
                capture_output=True, text=True, encoding="utf-8", timeout=timeout,
            )

            if compile_process.returncode != 0:
                translated_error = localize_rust_errors(compile_process.stderr).replace(str(rs_filepath), str(source_path))

                print("\n" + "=" * 60)
                print("AN SAMI KUSKUREN RUSTC YAYIN HADASWA (Compilation Error):")
                print(translated_error, end="")
                print("=" * 60 + "\n")
                return compile_process.returncode

            run_process = subprocess.run(
                [str(exe_filepath.resolve())], capture_output=True, text=True,
                encoding="utf-8", timeout=timeout,
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

    except subprocess.TimeoutExpired:
        print(f"KUSKURE: Shirin ya wuce iyakar lokaci na dakika {timeout}.")
        return 124


def localize_rust_errors(error_text):
    """Translate known rustc message fragments into Hausa explanations."""
    translated = error_text
    for english, hausa in RUST_ERRORS.items():
        translated = re.sub(re.escape(english), hausa, translated, flags=re.IGNORECASE)
    return translated
