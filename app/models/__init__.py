"""
Importing all models here means that when we import app.models anywhere,
SQLAlchemy knows about every table and can create them all together.
"""

from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.borrow_record import BorrowRecord