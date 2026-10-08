
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass

class BookPatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=1, max_length=100)
    year: int | None = Field(None, ge=0)

class Book(BookBase):
    id: int
