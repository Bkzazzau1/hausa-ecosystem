from pathlib import Path

PROJECT_GENERATOR_USAGE = (
    "Kuskure: Yi amfani da:\n"
    "  hausa new backend flask my_api\n"
    "  hausa new backend fastapi my_api\n"
    "  hausa new database sqlite my_db_app"
)

FLASK_APP = '''# Hausa Flask backend CRUD project
# Run: hausa run app.hausa

daga flask shigo Injin_Yanar_Gizo, juya_zuwa_json, bukata
daga sqlite3 shigo bude_rufa

injin = Injin_Yanar_Gizo(__name__)
DATABASE = "app.db"


aiki samun_hadi():
    hadi = bude_rufa(DATABASE)
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("""
        CREATE TABLE IF NOT EXISTS abubuwa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suna TEXT NOT NULL
        )
    """)
    hadi.ajiye()
    mayar hadi


aiki maida_abu(layi):
    idan ba layi:
        mayar babu
    mayar {"id": layi[0], "suna": layi[1]}


aiki nemo_abu_daga_db(abu_id):
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("SELECT id, suna FROM abubuwa WHERE id = ?", (abu_id,))
    abu = maida_abu(mai_aiki.karba_guda())
    hadi.rufe()
    mayar abu


@injin.bude_hanya("/", methods=["GET"])
aiki gida():
    mayar juya_zuwa_json({"sako": "Hausa Flask CRUD backend yana aiki"})


@injin.bude_hanya("/abubuwa", methods=["GET"])
aiki duk_abubuwa():
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("SELECT id, suna FROM abubuwa ORDER BY id DESC")
    sakamako = mai_aiki.karba_duka()
    hadi.rufe()

    mayar juya_zuwa_json([maida_abu(layi) ga layi cikin sakamako])


@injin.bude_hanya("/abubuwa", methods=["POST"])
aiki kirkiri_abu():
    bayanai = bukata.karanta_json() ko {}
    suna = bayanai.samu("suna")

    idan ba suna:
        mayar juya_zuwa_json({"kuskure": "suna ya zama dole"}), 400

    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("INSERT INTO abubuwa (suna) VALUES (?)", (suna,))
    hadi.ajiye()
    sabon_id = mai_aiki.sabon_id
    hadi.rufe()

    mayar juya_zuwa_json({"id": sabon_id, "suna": suna}), 201


@injin.bude_hanya("/abubuwa/<int:abu_id>", methods=["GET"])
aiki samu_abu(abu_id):
    abu = nemo_abu_daga_db(abu_id)
    idan ba abu:
        mayar juya_zuwa_json({"kuskure": "Ba a sami abu ba"}), 404
    mayar juya_zuwa_json(abu)


@injin.bude_hanya("/abubuwa/<int:abu_id>", methods=["PUT"])
aiki sabunta_abu(abu_id):
    abu = nemo_abu_daga_db(abu_id)
    idan ba abu:
        mayar juya_zuwa_json({"kuskure": "Ba a sami abu ba"}), 404

    bayanai = bukata.karanta_json() ko {}
    suna = bayanai.samu("suna")
    idan ba suna:
        mayar juya_zuwa_json({"kuskure": "suna ya zama dole"}), 400

    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("UPDATE abubuwa SET suna = ? WHERE id = ?", (suna, abu_id))
    hadi.ajiye()
    hadi.rufe()

    mayar juya_zuwa_json({"id": abu_id, "suna": suna})


@injin.bude_hanya("/abubuwa/<int:abu_id>", methods=["DELETE"])
aiki goge_abu(abu_id):
    abu = nemo_abu_daga_db(abu_id)
    idan ba abu:
        mayar juya_zuwa_json({"kuskure": "Ba a sami abu ba"}), 404

    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("DELETE FROM abubuwa WHERE id = ?", (abu_id,))
    hadi.ajiye()
    hadi.rufe()

    mayar juya_zuwa_json({"sako": "An goge abu", "abu": abu})


idan __name__ == "__main__":
    injin.run(host="127.0.0.1", port=5000, debug=gaskiya)
'''

FASTAPI_APP = '''# Hausa FastAPI backend CRUD project
# Run: hausa run app.hausa

daga fastapi shigo Saurin_API, Kuskuren_HTTP
daga pydantic shigo Tushen_Model
shigo Sabar_Uvicorn

app = Saurin_API(title="Hausa FastAPI CRUD Backend")


aji Abu(Tushen_Model):
    suna: rubutu


abubuwa = []


aiki nemo_abu(abu_id: lamba):
    ga abu cikin abubuwa:
        idan abu["id"] == abu_id:
            mayar abu
    mayar babu


@app.samu("/")
aiki gida():
    mayar {"sako": "Hausa FastAPI CRUD backend yana aiki"}


@app.samu("/abubuwa")
aiki duk_abubuwa():
    mayar abubuwa


@app.aika("/abubuwa", status_code=201)
aiki kirkiri_abu(abu: Abu):
    sabon_abu = abu.model_dump()
    sabon_abu["id"] = len(abubuwa) + 1
    abubuwa.append(sabon_abu)
    mayar sabon_abu


@app.samu("/abubuwa/{abu_id}")
aiki samu_abu(abu_id: lamba):
    abu = nemo_abu(abu_id)
    idan ba abu:
        tada Kuskuren_HTTP(status_code=404, detail="Ba a sami abu ba")
    mayar abu


@app.saka("/abubuwa/{abu_id}")
aiki sabunta_abu(abu_id: lamba, sabon_bayani: Abu):
    abu = nemo_abu(abu_id)
    idan ba abu:
        tada Kuskuren_HTTP(status_code=404, detail="Ba a sami abu ba")

    abu["suna"] = sabon_bayani.suna
    mayar abu


@app.goge_hanya("/abubuwa/{abu_id}")
aiki goge_abu(abu_id: lamba):
    abu = nemo_abu(abu_id)
    idan ba abu:
        tada Kuskuren_HTTP(status_code=404, detail="Ba a sami abu ba")

    abubuwa.remove(abu)
    mayar {"sako": "An goge abu", "abu": abu}


idan __name__ == "__main__":
    Sabar_Uvicorn.gudanar(app, host="127.0.0.1", port=8000)
'''

SQLITE_APP = '''# Hausa SQLite database CRUD project
# Run: hausa run app.hausa

daga sqlite3 shigo bude_rufa

DATABASE = "app.db"


aiki samun_hadi():
    hadi = bude_rufa(DATABASE)
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("""
        CREATE TABLE IF NOT EXISTS abubuwa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suna TEXT NOT NULL
        )
    """)
    hadi.ajiye()
    mayar hadi


aiki kirkiri_abu(suna):
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("INSERT INTO abubuwa (suna) VALUES (?)", (suna,))
    hadi.ajiye()
    sabon_id = mai_aiki.sabon_id
    hadi.rufe()
    mayar sabon_id


aiki duk_abubuwa():
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("SELECT id, suna FROM abubuwa ORDER BY id DESC")
    sakamako = mai_aiki.karba_duka()
    hadi.rufe()
    mayar sakamako


aiki samu_abu(abu_id):
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("SELECT id, suna FROM abubuwa WHERE id = ?", (abu_id,))
    sakamako = mai_aiki.karba_guda()
    hadi.rufe()
    mayar sakamako


aiki sabunta_abu(abu_id, suna):
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("UPDATE abubuwa SET suna = ? WHERE id = ?", (suna, abu_id))
    hadi.ajiye()
    layuka = mai_aiki.layuka
    hadi.rufe()
    mayar layuka


aiki goge_abu(abu_id):
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("DELETE FROM abubuwa WHERE id = ?", (abu_id,))
    hadi.ajiye()
    layuka = mai_aiki.layuka
    hadi.rufe()
    mayar layuka


idan __name__ == "__main__":
    na_farko = kirkiri_abu("Abu na farko")
    na_biyu = kirkiri_abu("Abu na biyu")

    buga("Bayan kirkira:")
    ga abu cikin duk_abubuwa():
        buga(abu)

    sabunta_abu(na_farko, "Abu na farko da aka sabunta")
    goge_abu(na_biyu)

    buga("Bayan sabuntawa da gogewa:")
    ga abu cikin duk_abubuwa():
        buga(abu)
'''

PROJECT_TEMPLATES = {
    ("backend", "flask"): {
        "description": "Hausa Flask CRUD backend API project",
        "files": {
            "app.hausa": FLASK_APP,
            "requirements.txt": "flask\n",
            "README.md": "# Hausa Flask CRUD Backend\n\nRun:\n\n```bash\npip install -r requirements.txt\nhausa run app.hausa\n```\n\nEndpoints:\n\n- GET /\n- GET /abubuwa\n- POST /abubuwa\n- GET /abubuwa/<id>\n- PUT /abubuwa/<id>\n- DELETE /abubuwa/<id>\n",
        },
    },
    ("backend", "fastapi"): {
        "description": "Hausa FastAPI CRUD backend API project",
        "files": {
            "app.hausa": FASTAPI_APP,
            "requirements.txt": "fastapi\nuvicorn\n",
            "README.md": "# Hausa FastAPI CRUD Backend\n\nRun:\n\n```bash\npip install -r requirements.txt\nhausa run app.hausa\n```\n\nOpen API docs:\n\n```text\nhttp://127.0.0.1:8000/docs\n```\n",
        },
    },
    ("database", "sqlite"): {
        "description": "Hausa SQLite database CRUD project",
        "files": {
            "app.hausa": SQLITE_APP,
            "requirements.txt": "",
            "README.md": "# Hausa SQLite Database CRUD App\n\nRun:\n\n```bash\nhausa run app.hausa\n```\n",
        },
    },
}


def is_project_generator_request(args):
    return bool(args) and args[0] in ("backend", "database")


def create_project(args):
    if len(args) != 3:
        print(PROJECT_GENERATOR_USAGE)
        return 1

    category, template_name, project_dir = args
    template = PROJECT_TEMPLATES.get((category, template_name))
    if template is None:
        print(PROJECT_GENERATOR_USAGE)
        return 1

    target_dir = Path(project_dir)
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"Kuskure: Folder din ba komai bane: {target_dir}")
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)

    for relative_path, content in template["files"].items():
        file_path = target_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    print(f"An kirkiro project: {target_dir}")
    print(template["description"])
    print("Mataki na gaba:")
    print(f"  cd {target_dir}")
    print("  hausa run app.hausa")
    return 0
