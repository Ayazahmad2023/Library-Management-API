from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """What the client sends us to register."""
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """What we send back — notice: NO password field at all."""
    id: int
    username: str
    email: str
    is_admin: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """What the client sends us to log in."""
    username: str
    password: str
     