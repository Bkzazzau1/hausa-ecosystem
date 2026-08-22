# core/database.py
import os
import sqlite3
from pathlib import Path


def user_data_directory():
    """Return a writable per-user data directory without touching the install."""
    configured = os.environ.get("HAUSA_DATA_DIR")
    if configured:
        return Path(configured).expanduser()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "hausa-ecosystem"


DB_PATH = user_data_directory() / "vocabulary.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Creates tables and populates them with our master dictionary data."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS python_keywords (
            hausa_word TEXT PRIMARY KEY,
            english_word TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rust_keywords (
            hausa_word TEXT PRIMARY KEY,
            english_word TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_errors (
            error_key TEXT PRIMARY KEY,
            hausa_translation TEXT NOT NULL
        )
    """)

    from core.dictionary import PYTHON_ERRORS, PYTHON_KEYWORDS, RUST_ERRORS, RUST_KEYWORDS

    seed_table(cursor, "python_keywords", PYTHON_KEYWORDS, "hausa_word", "english_word")
    seed_table(cursor, "rust_keywords", RUST_KEYWORDS, "hausa_word", "english_word")
    seed_table(cursor, "system_errors", {**PYTHON_ERRORS, **RUST_ERRORS}, "error_key", "hausa_translation")

    conn.commit()
    conn.close()


def seed_table(cursor, table_name, data_dict, key_col, val_col):
    for key, value in data_dict.items():
        cursor.execute(
            f"INSERT OR IGNORE INTO {table_name} ({key_col}, {val_col}) VALUES (?, ?)",
            (key, value),
        )


def load_dictionary_from_db():
    """Load built-ins plus optional overrides from a per-user database.

    Importing Hausa Ecosystem never creates files.  A database is read only
    when the user has explicitly initialized one.
    """
    from core.dictionary import PYTHON_ERRORS, PYTHON_KEYWORDS, RUST_ERRORS, RUST_KEYWORDS

    py_keywords = dict(PYTHON_KEYWORDS)
    rust_keywords = dict(RUST_KEYWORDS)
    errors = {**PYTHON_ERRORS, **RUST_ERRORS}
    if not DB_PATH.exists():
        return py_keywords, rust_keywords, errors

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT hausa_word, english_word FROM python_keywords")
        py_keywords.update(cursor.fetchall())
        cursor.execute("SELECT hausa_word, english_word FROM rust_keywords")
        rust_keywords.update(cursor.fetchall())
        cursor.execute("SELECT error_key, hausa_translation FROM system_errors")
        errors.update(cursor.fetchall())
    finally:
        conn.close()
    # Normalize a mojibake alias written by pre-1.0 development databases.
    # Keep the ASCII spelling too, but never expose the corrupted token.
    if "buÆ™ata" in py_keywords:
        py_keywords.setdefault("buƙata", py_keywords["buÆ™ata"])
        del py_keywords["buÆ™ata"]
    return py_keywords, rust_keywords, errors
