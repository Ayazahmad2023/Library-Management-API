from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from app.schemas.borrow import BorrowCreate, BorrowOut
from app.utils.security import get_current_user, require_admin

router = APIRouter(prefix="/borrow", tags=["Borrow Records"])

LOAN_PERIOD_DAYS = 14


@router.post("/", response_model=BorrowOut, status_code=201)
def borrow_book(
    request: BorrowCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /borrow — borrow a book (must be logged in)."""
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No copies available to borrow")

    book.available_copies -= 1

    new_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book.id,
        due_at=datetime.now(timezone.utc) + timedelta(days=LOAN_PERIOD_DAYS),
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.put("/{record_id}/return", response_model=BorrowOut)
def return_book(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """PUT /borrow/{id}/return — return a borrowed book (must be the borrower)."""
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This isn't your borrow record")
    if record.is_returned:
        raise HTTPException(status_code=400, detail="This book was already returned")

    record.is_returned = True
    record.returned_at = datetime.now(timezone.utc)
    record.book.available_copies += 1

    db.commit()
    db.refresh(record)
    return record


@router.get("/my-history", response_model=List[BorrowOut])
def my_borrow_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """GET /borrow/my-history — see everything I've ever borrowed."""
    return db.query(BorrowRecord).filter(BorrowRecord.user_id == current_user.id).all()


@router.get("/active", response_model=List[BorrowOut])
def all_active_borrows(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    """GET /borrow/active — admin only: see every book currently checked out."""
    return db.query(BorrowRecord).filter(BorrowRecord.is_returned == False).all()


@router.get("/overdue", response_model=List[BorrowOut])
def overdue_borrows(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    """GET /borrow/overdue — admin only: see books that are overdue."""
    now = datetime.now(timezone.utc)
    return db.query(BorrowRecord).filter(
        BorrowRecord.is_returned == False,
        BorrowRecord.due_at < now,
    ).all()