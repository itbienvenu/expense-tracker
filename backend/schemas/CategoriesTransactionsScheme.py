from pydantic import BaseModel, constr
from uuid import UUID
from typing import List, Optional
from datetime import date, datetime


# Category

class CategoryCreate(BaseModel):
    name: constr(min_length=1, max_length=50)

class CategoryResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


# Transaction

class TransactionCreate(BaseModel):
    title: constr(min_length=1, max_length=100)
    amount: float
    date: Optional[datetime] = None
    category_ids: List[UUID]

class TransactionResponse(BaseModel):
    id: UUID
    title: str
    amount: float
    date: date
    categories: List[CategoryResponse]

    class Config:
        orm_mode = True

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    category_ids: Optional[List[UUID]] = None