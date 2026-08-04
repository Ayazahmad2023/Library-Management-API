from pydantic import BaseModel
from typing import Optional
from app.schemas.author import AuthorOut


class BookCreate(BaseModel):
    """What the client must send us to create a book."""
    title: str
    isbn: Optional[str] = None
    total_copies: int = 1
    author_id: int


class BookOut(BaseModel):
    """What we send back to the client."""
    id: int
    title: str
    isbn: Optional[str] = None
    total_copies: int
    available_copies: int
    author: AuthorOut  # nested schema — shows full author details, not just an id

    class Config:
        from_attributes = True