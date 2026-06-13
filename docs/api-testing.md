# API Testing Command

Hausa Ecosystem can test generated Flask and FastAPI CRUD APIs from the command line.

Start a generated Flask backend in one terminal:

```bash
hausa new backend flask my_flask_crud
cd my_flask_crud
pip install -r requirements.txt
hausa run app.hausa
```

Then test it from another terminal:

```bash
hausa test-api flask http://127.0.0.1:5000
```

Start a generated FastAPI backend in one terminal:

```bash
hausa new backend fastapi my_fastapi_crud
cd my_fastapi_crud
pip install -r requirements.txt
hausa run app.hausa
```

Then test it from another terminal:

```bash
hausa test-api fastapi http://127.0.0.1:8000
```

The command checks:

```text
GET /
GET /abubuwa
POST /abubuwa
GET /abubuwa/{id}
PUT /abubuwa/{id}
DELETE /abubuwa/{id}
GET deleted /abubuwa/{id} returns 404
```

A successful run ends with:

```text
Sakamako: 7 passed, 0 failed
```
