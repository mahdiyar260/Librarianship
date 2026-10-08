
from fastapi import APIRouter, HTTPException, Request, Response, status
import hashlib
import json

from app.schemas.book import Book, BookCreate, BookPatch, BookUpdate
from app.services.book_service import book_service

router = APIRouter(prefix="/books", tags=["books"])

NOT_FOUND = {"description": "Book not found"}
SERVER_ERROR = {"description": "Internal server error"}


def _build_etag(books: list[Book]) -> str:
    """Hash of the current books list, used to detect changes."""
    payload = json.dumps([book.model_dump() for book in books], sort_keys=True)
    return f'"{hashlib.sha256(payload.encode()).hexdigest()[:16]}"'


@router.post(
    "",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Book created"},
        422: {"description": "Validation error"},
        500: SERVER_ERROR,
    },
)
def create_book(data: BookCreate) -> Book:
    return book_service.create(data)


@router.get(
    "",
    response_model=list[Book],
    responses={
        200: {"description": "List of all books"},
        304: {"description": "Not modified, use the cached version"},
        500: SERVER_ERROR,
    },
)
def list_books(request: Request, response: Response) -> list[Book] | Response:
    books = book_service.list_all()
    etag = _build_etag(books)
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers={"ETag": etag})
    response.headers["ETag"] = etag
    return books


# Must be declared before "/{book_id}", otherwise "search" is read as a book_id.
@router.get(
    "/search",
    responses={
        501: {"description": "Not implemented yet"},
    },
)
def search_books() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Search is not implemented yet")


@router.get(
    "/{book_id}",
    response_model=Book,
    responses={
        200: {"description": "Book found"},
        404: NOT_FOUND,
        422: {"description": "Validation error"},
        500: SERVER_ERROR,
    },
)
def get_book(book_id: int) -> Book:
    book = book_service.get(book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return book


@router.patch(
    "/{book_id}",
    response_model=Book,
    responses={
        200: {"description": "Book updated"},
        404: NOT_FOUND,
        422: {"description": "Validation error"},
        500: SERVER_ERROR,
    },
)
def patch_book(book_id: int, data: BookPatch) -> Book:
    book = book_service.get(book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    merged = {**book.model_dump(exclude={"id"}), **data.model_dump(exclude_none=True)}
    return book_service.update(book_id, BookUpdate(**merged))


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Book deleted"},
        404: NOT_FOUND,
        422: {"description": "Validation error"},
        500: SERVER_ERROR,
    },
)
def delete_book(book_id: int) -> Response:
    if book_service.delete(book_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)