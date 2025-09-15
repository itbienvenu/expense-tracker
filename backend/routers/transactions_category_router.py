from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database.models import Category, Transaction, User
from schemas.CategoriesTransactionsScheme import CategoryCreate, CategoryResponse, TransactionCreate, TransactionResponse, TransactionUpdate
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
) -> UUID:
    existing = db.query(Category).filter(Category.name == category.name, Category.user_id == UUID(user_id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = Category(name=category.name, user_id=UUID(user_id))
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Endpoint to update category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id, 
    category: CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    db_category = db.query(Category).filter(
        Category.id == UUID(category_id), 
        Category.user_id == UUID(current_user)
    ).first()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


# Endpoint to delete category

@router.delete("/categories/{category_id}")
def delete_category(category_id, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.id == UUID(category_id), Category.user_id == UUID(current_user)).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return {"detail":"Category deleted"}

# lIST CATEGORIES

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


# Transaction update endpoint
@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
def patch_transaction(
    transaction_id,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_transaction = db.query(Transaction).filter(
        Transaction.id == UUID(transaction_id),
        Transaction.user_id == UUID(current_user)
    ).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # update provided fields only
    if transaction.title is not None:
        db_transaction.title = transaction.title
    if transaction.amount is not None:
        db_transaction.amount = transaction.amount
    if transaction.date is not None:
        db_transaction.date = transaction.date
    if transaction.category_ids is not None:
        categories = db.query(Category).filter(
            Category.id.in_(transaction.category_ids),
            Category.user_id == current_user
        ).all()
        if not categories or len(categories) != len(transaction.category_ids):
            raise HTTPException(status_code=400, detail="Invalid categories")
        db_transaction.categories = categories

    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Endpoint to delete transaction

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_transaction = db.query(Transaction).filter(Transaction.id == UUID(transaction_id), Transaction.user_id == UUID(current_user)).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(db_transaction)
    db.commit()
    return {"detail":"Transaction deleted"}