# core/python_engine.py
import io
import re
import sys
import tokenize
import traceback
from pathlib import Path

from core.database import load_dictionary_from_db

# Load tokens directly from SQLite live database entries.
PYTHON_KEYWORDS, _, PYTHON_ERRORS = load_dictionary_from_db()

# Create the reverse map dynamically for English-to-Hausa translation
REVERSE_PYTHON_KEYWORDS = {v: k for k, v in PYTHON_KEYWORDS.items()}

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
    except tokenize.TokenError:
        for key in sorted(mapping.keys(), key=len, reverse=True):
            pattern = r'\b' + re.escape(key) + r'\b'
            text = re.sub(pattern, mapping[key], text)
        return text

def hausa_to_english(hausa_code):
    return translate_logic(hausa_code, PYTHON_KEYWORDS)

def english_to_hausa(english_code):
    return translate_logic(english_code, REVERSE_PYTHON_KEYWORDS)

def translate_source(source):
    return hausa_to_english(source)

def translate_file(filepath):
    return translate_source(Path(filepath).read_text(encoding='utf-8'))

def run_file(filepath):
    return run_hausa_code(filepath)

def run_hausa_code(filepath):
    """Executes a .hausa file natively and outputs custom Hausa error logs."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            hausa_source = f.read()
    except FileNotFoundError:
        print(f"Kuskure: Ba a sami fayil din ba a: {filepath}")
        return 1

    # Convert to standard Python execution string
    english_source = hausa_to_english(hausa_source)

    try:
        compiled_code = compile(english_source, filepath, 'exec')
        runtime_globals = {
            "__name__": "__main__",
            "__file__": str(Path(filepath).resolve()),
        }
        exec(compiled_code, runtime_globals)
        return 0
    except Exception as e:
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
        print(f"Bayani na Turanci: {error_details}")
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
