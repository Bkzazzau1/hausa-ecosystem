# Backend and Database Tools

Hausa Ecosystem now includes Hausa words for common backend and database work.

## SQLite database words

| Hausa | Python |
| --- | --- |
| `bude_rufa` | `connect` |
| `samu_cursor` | `cursor` |
| `aiwatar` | `execute` |
| `aiwatar_da_yawa` | `executemany` |
| `karba_guda` | `fetchone` |
| `karba_duka` | `fetchall` |
| `ajiye` | `commit` |
| `janye` | `rollback` |
| `rufe` | `close` |
| `sabon_id` | `lastrowid` |

## Backend route words

| Hausa | Python/backend meaning |
| --- | --- |
| `Injin_Yanar_Gizo` | `Flask` |
| `bude_hanya` | `route` |
| `bukata` / `buƙata` | `request` |
| `juya_zuwa_json` | `jsonify` |
| `karanta_json` | `get_json` |
| `samu` | `get` |
| `aika` | `post` |
| `saka` | `put` |
| `gyara_sashe` | `patch` |
| `goge_hanya` | `delete` |

## FastAPI words

| Hausa | Python/backend meaning |
| --- | --- |
| `Saurin_API` | `FastAPI` |
| `Mai_Hanya` | `APIRouter` |
| `Kuskuren_HTTP` | `HTTPException` |
| `Dogaro` | `Depends` |
| `Tushen_Model` | `BaseModel` |
| `Filin` | `Field` |
| `Sabar_Uvicorn` | `uvicorn` |
| `gudanar` | `run` |

## Examples

Run the SQLite example:

```bash
hausa run templates/database_app.hausa
```

Translate the Flask API example:

```bash
hausa to-en templates/backend_flask_api.hausa -o backend_flask_api.py
```

Translate the FastAPI example:

```bash
hausa to-en templates/backend_fastapi.hausa -o backend_fastapi.py
```

The examples may create local `.db` files when they are executed. Those files are ignored by Git.
