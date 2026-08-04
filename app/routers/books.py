from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookOut

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookOut, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """POST /books — create a new book."""
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = Book(
        title=book.title,
        isbn=book.isbn,
        total_copies=book.total_copies,
        available_copies=book.total_copies,  # all copies start out available
        author_id=book.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=List[BookOut])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """GET /books — list books, with pagination."""
    return db.query(Book).offset(skip).limit(limit).all()


@router.get("/search", response_model=List[BookOut])
def search_books(title: str, db: Session = Depends(get_db)):
    """GET /books/search?title=... — search books by (partial) title."""
    return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()


@router.get("/by-author/{author_id}", response_model=List[BookOut])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    """GET /books/by-author/{author_id} — list all books by one author."""
    return db.query(Book).filter(Book.author_id == author_id).all()


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """GET /books/{id} — get one book by id."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated: BookCreate, db: Session = Depends(get_db)):
    """PUT /books/{id} — update a book's details."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = updated.title
    book.isbn = updated.isbn
    book.total_copies = updated.total_copies
    book.author_id = updated.author_id
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """DELETE /books/{id} — remove a book."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None