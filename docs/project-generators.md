# Project Generators

Hausa Ecosystem can generate starter backend and database projects. The generated backend projects include basic CRUD endpoints: create, list, detail, update, and delete.

## Flask CRUD backend

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

Example endpoints:

```text
GET    /
GET    /abubuwa
POST   /abubuwa
GET    /abubuwa/<id>
PUT    /abubuwa/<id>
DELETE /abubuwa/<id>
```

## FastAPI CRUD backend

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

Example endpoints:

```text
GET    /
GET    /abubuwa
POST   /abubuwa
GET    /abubuwa/{abu_id}
PUT    /abubuwa/{abu_id}
DELETE /abubuwa/{abu_id}
```

## SQLite database CRUD app

```bash
hausa new database sqlite my_db_app
cd my_db_app
hausa run app.hausa
```

The SQLite generator creates `app.db` when the app runs. Database files are ignored by Git.

The generated SQLite app includes functions for:

```text
kirkiri_abu
samu_abu
duk_abubuwa
sabunta_abu
goge_abu
```
