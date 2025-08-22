## TodoList API (FastAPI)

Simple Todo List backend built with FastAPI, SQLAlchemy (SQLite), and Pydantic v2.

### Requirements
- Python 3.10+

### Project layout
```
todolist/                 # Project root (your current folder)
  ├─ todolist/            # Python package with the app code
  │  ├─ app/
  │  │  ├─ main.py        # FastAPI app + routes
  │  │  ├─ database.py    # SQLAlchemy engine/session
  │  │  ├─ models.py      # ORM models
  │  │  ├─ schemas.py     # Pydantic models
  │  │  └─ crud.py        # DB operations
  │  └─ requirements.txt  # Python dependencies
  └─ todolist.db          # SQLite database (auto-created on first run)
```

### Setup (Windows / Git Bash or PowerShell)
From the project root (this folder):
```bash
python -m venv .venv
source .venv/Scripts/activate   # PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r todolist/requirements.txt
```

### Run (development)
Run from the project root:
```bash
uvicorn todolist.app.main:app --reload
```

- App: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

To change host/port:
```bash
uvicorn todolist.app.main:app --reload --host 0.0.0.0 --port 8001
uvicorn todolist.app.main:app --host 127.0.0.1 --port 0
```

### Database
- SQLite file: `todolist.db` in the project root.
- To reset data, stop the server and delete `todolist.db`.

### API Reference

1) Create todo
```http
POST /todos
Content-Type: application/json
{
  "title": "Buy milk",
  "description": "2% organic",
  "completed": false,
  "due_at": "2025-01-31T17:00:00Z"
}
```
Response 201:
```json
{
  "id": 1,
  "title": "Buy milk",
  "description": "2% organic",
  "completed": false,
  "due_at": "2025-01-31T17:00:00+00:00",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": null
}
```

2) List todos
```http
GET /todos?skip=0&limit=100&due_before=2025-02-01T00:00:00Z&due_after=2025-01-01T00:00:00Z
```
Response 200:
```json
[
  { "id": 1, "title": "Buy milk", "description": "2% organic", "completed": false, "due_at": "2025-01-31T17:00:00+00:00", "created_at": "...", "updated_at": null }
]
```

3) Get a todo by id
```http
GET /todos/1
```
Response 200: same shape as create response. 404 if not found.

4) Update (partial)
```http
PATCH /todos/1
Content-Type: application/json
{
  "completed": true,
  "due_at": "2025-02-15T09:00:00Z"
}
```
Response 200: updated todo.

5) Delete
```http
DELETE /todos/1
```
Response 204 No Content.

### cURL examples
```bash
# Create
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2% organic", "due_at": "2025-01-31T17:00:00Z"}'

# List
curl http://127.0.0.1:8000/todos

# Get by id
curl http://127.0.0.1:8000/todos/1

# Update
curl -X PATCH http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true, "due_at": "2025-02-15T09:00:00Z"}'

# Delete
curl -X DELETE http://127.0.0.1:8000/todos/1 -i
```

### Notes
- Autoreload is enabled in dev; edits restart the server.
- CORS is open for simplicity. Lock it down in production.
- No migrations are used; tables are created at startup.

alembic revision --autogenerate -m "create todolist model"
alembic upgrade head