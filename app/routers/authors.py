from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorOut

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorOut, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """POST /authors — create a new author."""
    new_author = Author(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=List[AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    """GET /authors — list every author."""
    return db.query(Author).all()


@router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """GET /authors/{id} — get one author by id."""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorOut)
def update_author(author_id: int, updated: AuthorCreate, db: Session = Depends(get_db)):
    """PUT /authors/{id} — update an author's details."""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author.name = updated.name
    author.bio = updated.bio
    db.commit()
    db.refresh(author)
    return author


@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """DELETE /authors/{id} — remove an author."""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return None