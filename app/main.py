
from fastapi import FastAPI

from app.routers import books

app = FastAPI(title="Librarianship")

app.include_router(books.router)
