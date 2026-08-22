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

## Django starter

```bash
hausa new backend django my_site
cd my_site
pip install -r requirements.txt
hausa to-en main/views.hausa -o main/views.py --profile django
python manage.py check
python manage.py runserver
```

The generated project keeps Django's normal `manage.py`, settings, and URL
layout. Edit `main/views.hausa`, translate it to `main/views.py`, and then run
Django. Replace the example secret and configure allowed hosts before production.

The generated SQLite app includes functions for:

```text
kirkiri_abu
samu_abu
duk_abubuwa
sabunta_abu
goge_abu
```
# Project generators

Generated projects are secure learning baselines, not complete production
deployments. They use bounded dependency ranges, environment-based host/port and
database settings, persistent SQLite data where applicable, disabled Flask debug
mode, an `.env.example`, and a starter test.

Create and prepare a project:

```bash
hausa new backend flask my_api
cd my_api
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest
hausa run app.hausa --profile flask
```

Before internet-facing deployment, add authentication, authorization, HTTPS,
secret management, database migrations, request limits, structured logging,
backups, and a production process manager appropriate to the chosen framework.
