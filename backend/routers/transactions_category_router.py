from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database.models import Category, Transaction, User
from schemas.CategoriesTransactionsScheme import CategoryCreate, CategoryResponse, TransactionCreate, TransactionResponse
from database.dbs import get_db
from methods.functions import get_current_user

from uuid import UUID

router = APIRouter(prefix="/tracker", tags=["Expense Tracker"])


# Create Category

@router.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    existing = db.query(Category).filter(Category.name == category.name, Category.user_id == UUID(user_id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = Category(name=category.name, user_id=UUID(user_id))
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# List Categories

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return db.query(Category).filter(Category.user_id == UUID(user_id)).all()


# Create Transaction

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    categories = db.query(Category).filter(
        Category.id.in_(transaction.category_ids),
        Category.user_id == UUID(user_id)
    ).all()
    if not categories or len(categories) != len(transaction.category_ids):
        raise HTTPException(status_code=400, detail="Invalid categories")
    
    new_transaction = Transaction(
        title=transaction.title,
        amount=transaction.amount,
        date=transaction.date or date.today(),
        user_id=UUID(user_id),
        categories=categories
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


# List Transactions
@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return db.query(Transaction).filter(Transaction.user_id == UUID(user_id)).all()
