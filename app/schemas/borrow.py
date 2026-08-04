from pydantic import BaseModel
from datetime import datetime
from app.schemas.book import BookOut


class BorrowCreate(BaseModel):
    """What the client sends to borrow a book — just which book."""
    book_id: int


class BorrowOut(BaseModel):
    """What we send back describing one borrow record."""
    id: int
    book: BookOut
    borrowed_at: datetime
    due_at: datetime
    returned_at: datetime | None = None
    is_returned: bool

    class Config:
        from_attributes = True