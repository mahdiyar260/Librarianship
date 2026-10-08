# Librarianship

A simple FastAPI practice project: CRUD endpoints for a library of books.
Data is stored in memory (no database), so it resets when the server restarts.

## Project structure

```
library-api/
├── app/
│   ├── main.py              # FastAPI app and router registration
│   ├── routers/
│   │   └── books.py         # Book endpoints
│   ├── schemas/
│   │   └── book.py          # Pydantic models
│   └── services/
│       └── book_service.py  # In-memory storage and logic
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Interactive docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path          | Description      |
|--------|---------------|------------------|
| POST   | `/books`      | Create a book    |
| GET    | `/books`      | Get all books    |
| GET    | `/books/{id}` | Get one book     |
| PUT    | `/books/{id}` | Update a book    |
| DELETE | `/books/{id}` | Delete a book    |

Book body:

```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "year": 2008
}
```
