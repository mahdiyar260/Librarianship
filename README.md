# Librarianship

A simple FastAPI practice project: CRUD endpoints for books.
Data is stored in PostgreSQL (Docker Compose) and accessed with raw SQL via `psycopg`.

## Setup

1. Create a `.env` file next to `docker-compose.yml`:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=
```

Avoid special characters like `@`, `:` or `/` in the password.

2. Start the database (tables are created from `db/init.sql`):

```bash
docker compose up -d
```

3. Install dependencies and run:

```bash
python -m venv venv
venv\Scripts\activate           # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

> If you change the user, password or database name after the first run, recreate the volume:
> `docker compose down -v && docker compose up -d`

## Endpoints

| Method | Path          | Description             |
|--------|---------------|-------------------------|
| POST   | `/books`      | Create a book (201)     |
| GET    | `/books`      | Get all books           |
| GET    | `/books/{id}` | Get one book            |
| PATCH  | `/books/{id}` | Partially update a book |
| DELETE | `/books/{id}` | Delete a book (204)     |

Book body:

```json
{ "title": "Clean Code", "author": "Robert C. Martin", "year": 2008 }
```