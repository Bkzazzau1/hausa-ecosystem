# core/python_engine.py
import io
import re
import sys
import tokenize
import traceback
from pathlib import Path

from core.database import load_dictionary_from_db

# Load immutable built-ins plus any explicitly configured user overrides.
PYTHON_KEYWORDS, _, PYTHON_ERRORS = load_dictionary_from_db()

# Create the reverse map dynamically for English-to-Hausa translation
REVERSE_PYTHON_KEYWORDS = {v: k for k, v in PYTHON_KEYWORDS.items()}

class TranslationError(ValueError):
    """Raised when source cannot be tokenized without risking data corruption."""


def _mapping_for_profile(profile, reverse=False):
    from core.dictionary import get_python_vocabulary

    mapping = PYTHON_KEYWORDS if profile == "all" else get_python_vocabulary(profile)
    if not reverse:
        return mapping
    reverse_mapping = {}
    for hausa, english in mapping.items():
        # The first canonical spelling wins; aliases never silently replace it.
        reverse_mapping.setdefault(english, hausa)
    return reverse_mapping


def translate_logic(text, mapping):
    """Translate only Python name tokens, leaving strings and comments untouched."""
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        translated_tokens = []
        for token in tokens:
            if token.type == tokenize.NAME and token.string in mapping:
                token = token._replace(string=mapping[token.string])
            translated_tokens.append(token)
        return tokenize.untokenize(translated_tokens)
    except (tokenize.TokenError, IndentationError) as error:
        raise TranslationError(f"Ba a iya fassara rubutun da bai cika ba: {error}") from error

def hausa_to_english(hausa_code, profile="all"):
    return translate_logic(hausa_code, _mapping_for_profile(profile))

def english_to_hausa(english_code, profile="all"):
    return translate_logic(english_code, _mapping_for_profile(profile, reverse=True))

def translate_source(source):
    return hausa_to_english(source)

def translate_file(filepath):
    return translate_source(Path(filepath).read_text(encoding='utf-8'))

def run_file(filepath):
    return run_hausa_code(filepath)

def run_hausa_code(filepath, profile="all", verbose=False):
    """Executes a .hausa file natively and outputs custom Hausa error logs."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            hausa_source = f.read()
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeError) as error:
        print(f"Kuskure: Ba a iya karanta fayil din {filepath}: {error}")
        return 1

    # Convert to standard Python execution string
    try:
        english_source = hausa_to_english(hausa_source, profile=profile)
    except TranslationError as error:
        print(f"Kuskuren Fassara: {error}")
        return 1

    try:
        compiled_code = compile(english_source, filepath, 'exec')
        runtime_globals = {
            "__name__": "__main__",
            "__file__": str(Path(filepath).resolve()),
        }
        exec(compiled_code, runtime_globals)
        return 0
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_name = exc_type.__name__
        error_details = localize_error_details(str(exc_value))
        
        tb = traceback.extract_tb(exc_traceback)
        line_num = getattr(exc_value, "lineno", None) or (tb[-1].lineno if tb else "Babu sani")

        # Translate the error details using your new dictionary
        hausa_error_name = PYTHON_ERRORS.get(error_name, error_name)
        
        print("\n" + "="*50)
        print(f"AN SAMI KUSKURE A LAYI NA {line_num}!")
        print(f"Nau'in Kuskure: {hausa_error_name}")
        print(f"Bayani: {error_details}")
        if isinstance(line_num, int):
            source_lines = hausa_source.splitlines()
            if 1 <= line_num <= len(source_lines):
                source_line = source_lines[line_num - 1]
                print(f"  {source_line}")
                offset = max(1, getattr(exc_value, "offset", 1) or 1)
                print("  " + " " * (offset - 1) + "^")
        if verbose:
            print("Cikakken traceback:")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        print("="*50 + "\n")
        return 1


def localize_error_details(error_details):
    """Translate known substrings inside Python exception messages."""
    translated = error_details
    for english, hausa in PYTHON_ERRORS.items():
        if english.endswith("Error"):
            continue
        translated = re.sub(re.escape(english), hausa, translated, flags=re.IGNORECASE)
    return translated
