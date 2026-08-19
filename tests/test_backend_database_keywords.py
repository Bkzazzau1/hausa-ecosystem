from core.database import load_dictionary_from_db
from core.python_engine import english_to_hausa, hausa_to_english, run_hausa_code


def test_loaded_vocabulary_contains_no_mojibake():
    python_keywords, _, _ = load_dictionary_from_db()
    assert "buƙata" in python_keywords
    assert "buÆ™ata" not in python_keywords


def test_database_keywords_translate_to_sqlite_python():
    source = '''
daga sqlite3 shigo bude_rufa

hadi = bude_rufa("gwaji.db")
mai_aiki = hadi.samu_cursor()
mai_aiki.aiwatar("SELECT 1")
sakamako = mai_aiki.karba_guda()
hadi.ajiye()
hadi.rufe()
'''

    translated = hausa_to_english(source)

    assert "from sqlite3 import connect" in translated
    assert "hadi = connect" in translated
    assert "hadi.cursor()" in translated
    assert "mai_aiki.execute" in translated
    assert "mai_aiki.fetchone()" in translated
    assert "hadi.commit()" in translated
    assert "hadi.close()" in translated


def test_backend_keywords_translate_to_flask_and_fastapi_terms():
    source = '''
daga flask shigo Injin_Yanar_Gizo, juya_zuwa_json, bukata
daga fastapi shigo Saurin_API, Kuskuren_HTTP, Dogaro

injin = Injin_Yanar_Gizo(__name__)
app = Saurin_API()

@injin.bude_hanya("/dalibai", methods=["POST"])
aiki kirkiri():
    bayanai = bukata.karanta_json()
    mayar juya_zuwa_json(bayanai)

@app.samu("/dalibai")
aiki duk_dalibai():
    mayar []
'''

    translated = hausa_to_english(source)

    assert "from flask import Flask, jsonify, request" in translated
    assert "from fastapi import FastAPI, HTTPException, Depends" in translated
    assert "injin = Flask(__name__)" in translated
    assert "app = FastAPI()" in translated
    assert "@injin.route" in translated
    assert "request.get_json()" in translated
    assert "return jsonify" in translated
    assert "@app.get" in translated


def test_database_keywords_run_sqlite_workflow(tmp_path, capsys):
    db_path = (tmp_path / "dalibai.db").as_posix()
    source_file = tmp_path / "database_workflow.hausa"
    source_file.write_text(
        f'''
daga sqlite3 shigo bude_rufa

hadi = bude_rufa("{db_path}")
mai_aiki = hadi.samu_cursor()
mai_aiki.aiwatar("CREATE TABLE IF NOT EXISTS dalibai (id INTEGER PRIMARY KEY, suna TEXT)")
mai_aiki.aiwatar("INSERT INTO dalibai (suna) VALUES (?)", ("Bashir",))
hadi.ajiye()
mai_aiki.aiwatar("SELECT suna FROM dalibai")
buga(mai_aiki.karba_guda()[0])
hadi.rufe()
''',
        encoding="utf-8",
    )

    exit_code = run_hausa_code(str(source_file))
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Bashir" in captured.out


def test_english_backend_code_translates_back_to_hausa():
    source = '''
from sqlite3 import connect
from fastapi import FastAPI, HTTPException

app = FastAPI()
connection = connect("app.db")
cursor = connection.cursor()
cursor.execute("SELECT 1")
connection.commit()
connection.close()
'''

    translated = english_to_hausa(source)

    assert "daga sqlite3 shigo bude_rufa" in translated
    assert "daga fastapi shigo Saurin_API, Kuskuren_HTTP" in translated
    assert "app = Saurin_API()" in translated
    assert "connection = bude_rufa" in translated
    assert "connection.samu_cursor()" in translated
    assert "cursor.aiwatar" in translated
    assert "connection.ajiye()" in translated
    assert "connection.rufe()" in translated
