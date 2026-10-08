
from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.book import Book, BookCreate, BookPatch, BookUpdate
from app.services.book_service import book_service

router = APIRouter(prefix="/books", tags=["books"])

NOT_FOUND = {"description": "Book not found"}
SERVER_ERROR = {"description": "Internal server error"}


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
        500: SERVER_ERROR,
    },
)
def list_books() -> list[Book]:
    return book_service.list_all()


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