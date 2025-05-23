from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool
    created_at: datetime

    class Config:
        orm_mode = True

from typing import Optional

class BorrowCreate(BaseModel):
    user_id: int
    book_id: int

class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True
