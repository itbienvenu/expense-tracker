from pydantic import BaseModel, constr
from uuid import UUID
from typing import List, Optional
from datetime import date


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
    date: Optional[date] = None
    category_ids: List[UUID]

class TransactionResponse(BaseModel):
    id: UUID
    title: str
    amount: float
    date: date
    categories: List[CategoryResponse]

    class Config:
        orm_mode = True
