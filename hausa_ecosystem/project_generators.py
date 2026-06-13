from pathlib import Path

PROJECT_GENERATOR_USAGE = (
    "Kuskure: Yi amfani da:\n"
    "  hausa new backend flask my_api\n"
    "  hausa new backend fastapi my_api\n"
    "  hausa new database sqlite my_db_app"
)

FLASK_APP = '''# Hausa Flask backend project
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


@injin.bude_hanya("/", methods=["GET"])
aiki gida():
    mayar juya_zuwa_json({"sako": "Hausa Flask backend yana aiki"})


@injin.bude_hanya("/abubuwa", methods=["GET"])
aiki duk_abubuwa():
    hadi = samun_hadi()
    mai_aiki = hadi.samu_cursor()
    mai_aiki.aiwatar("SELECT id, suna FROM abubuwa ORDER BY id DESC")
    sakamako = mai_aiki.karba_duka()
    hadi.rufe()

    mayar juya_zuwa_json([
        {"id": layi[0], "suna": layi[1]}
        ga layi cikin sakamako
    ])


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


idan __name__ == "__main__":
    injin.run(host="127.0.0.1", port=5000, debug=gaskiya)
'''

FASTAPI_APP = '''# Hausa FastAPI backend project
# Run: hausa run app.hausa

daga fastapi shigo Saurin_API, Kuskuren_HTTP
daga pydantic shigo Tushen_Model
shigo Sabar_Uvicorn

app = Saurin_API(title="Hausa FastAPI Backend")


aji Abu(Tushen_Model):
    suna: rubutu


abubuwa = []


@app.samu("/")
aiki gida():
    mayar {"sako": "Hausa FastAPI backend yana aiki"}


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
    ga abu cikin abubuwa:
        idan abu["id"] == abu_id:
            mayar abu

    tada Kuskuren_HTTP(status_code=404, detail="Ba a sami abu ba")


idan __name__ == "__main__":
    Sabar_Uvicorn.gudanar(app, host="127.0.0.1", port=8000)
'''

SQLITE_APP = '''# Hausa SQLite database project
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


idan __name__ == "__main__":
    kirkiri_abu("Abu na farko")
    kirkiri_abu("Abu na biyu")

    ga abu cikin duk_abubuwa():
        buga(abu)
'''

PROJECT_TEMPLATES = {
    ("backend", "flask"): {
        "description": "Hausa Flask backend API project",
        "files": {
            "app.hausa": FLASK_APP,
            "requirements.txt": "flask\n",
            "README.md": "# Hausa Flask Backend\n\nRun:\n\n```bash\npip install -r requirements.txt\nhausa run app.hausa\n```\n",
        },
    },
    ("backend", "fastapi"): {
        "description": "Hausa FastAPI backend API project",
        "files": {
            "app.hausa": FASTAPI_APP,
            "requirements.txt": "fastapi\nuvicorn\n",
            "README.md": "# Hausa FastAPI Backend\n\nRun:\n\n```bash\npip install -r requirements.txt\nhausa run app.hausa\n```\n",
        },
    },
    ("database", "sqlite"): {
        "description": "Hausa SQLite database project",
        "files": {
            "app.hausa": SQLITE_APP,
            "requirements.txt": "",
            "README.md": "# Hausa SQLite Database App\n\nRun:\n\n```bash\nhausa run app.hausa\n```\n",
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
