from pydantic import BaseModel
from typing import Optional


class AuthorCreate(BaseModel):
    """What the client must send us to create an author."""
    name: str
    bio: Optional[str] = None


class AuthorOut(BaseModel):
    """What we send back to the client."""
    id: int
    name: str
    bio: Optional[str] = None

    class Config:
        from_attributes = True  # lets Pydantic read data straight from a SQLAlchemy model