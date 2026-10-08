
from app.schemas.book import Book, BookCreate, BookUpdate


class BookService:
    """In-memory storage for books."""

    def __init__(self) -> None:
        self._books: dict[int, Book] = {}
        self._next_id = 1

    def create(self, data: BookCreate) -> Book:
        book = Book(id=self._next_id, **data.model_dump())
        self._books[book.id] = book
        self._next_id += 1
        return book

    def get(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def list_all(self) -> list[Book]:
        return list(self._books.values())

    def update(self, book_id: int, data: BookUpdate) -> Book | None:
        if book_id not in self._books:
            return None
        book = Book(id=book_id, **data.model_dump())
        self._books[book_id] = book
        return book

    def delete(self, book_id: int) -> Book | None:
        return self._books.pop(book_id, None)


book_service = BookService()
