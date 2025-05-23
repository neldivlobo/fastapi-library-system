from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

from datetime import datetime

router = APIRouter(prefix="/borrows", tags=["Borrows"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.BorrowResponse)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    # Check if book exists and is available
    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    # Create borrow record
    new_borrow = models.Borrow(user_id=borrow.user_id, book_id=borrow.book_id)
    book.is_available = False  # Mark book as borrowed

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return new_borrow

@router.get("/", response_model=list[schemas.BorrowResponse])
def get_all_borrows(db: Session = Depends(get_db)):
    return db.query(models.Borrow).all()

@router.get("/{borrow_id}", response_model=schemas.BorrowResponse)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return borrow

@router.put("/{borrow_id}", response_model=schemas.BorrowResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    borrow.return_date = datetime.utcnow()

    # Mark the book as available again
    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if book:
        book.is_available = True

    db.commit()
    db.refresh(borrow)
    return borrow

@router.delete("/{borrow_id}")
def delete_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.return_date is None:
        raise HTTPException(status_code=400, detail="Cannot delete borrow record until book is returned")

    db.delete(borrow)
    db.commit()
    return {"message": "Borrow record deleted successfully"}
