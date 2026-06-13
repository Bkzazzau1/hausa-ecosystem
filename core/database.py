# core/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "hausa_tech.db"


def get_connection():
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
    """Queries the live database to build dynamic runtime conversion maps."""
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT hausa_word, english_word FROM python_keywords")
    py_keywords = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT hausa_word, english_word FROM rust_keywords")
    rust_keywords = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT error_key, hausa_translation FROM system_errors")
    errors = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return py_keywords, rust_keywords, errors


if not DB_PATH.exists():
    initialize_database()
