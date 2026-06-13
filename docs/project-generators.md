# Project Generators

Hausa Ecosystem can generate starter backend and database projects.

## Flask backend

```bash
hausa new backend flask my_api
cd my_api
pip install -r requirements.txt
hausa run app.hausa
```

Open:

```text
http://127.0.0.1:5000
http://127.0.0.1:5000/abubuwa
```

## FastAPI backend

```bash
hausa new backend fastapi my_api
cd my_api
pip install -r requirements.txt
hausa run app.hausa
```

Open:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

## SQLite database app

```bash
hausa new database sqlite my_db_app
cd my_db_app
hausa run app.hausa
```

The SQLite generator creates `app.db` when the app runs. Database files are ignored by Git.
