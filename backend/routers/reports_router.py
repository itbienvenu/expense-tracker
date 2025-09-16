from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from datetime import date

from database.dbs import get_db
from database.models import Transaction, Category
from methods.functions import get_current_user
from schemas.CategoriesTransactionsScheme import TransactionResponse

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/", response_model=List[TransactionResponse])
def get_filtered_transactions(
    start_date: Optional[date] = Query(None, description="Filter from this date"),
    end_date: Optional[date] = Query(None, description="Filter until this date"),
    category_ids: Optional[List[UUID]] = Query(None, description="Filter by category IDs"),
    min_amount: Optional[float] = Query(None, description="Minimum transaction amount"),
    max_amount: Optional[float] = Query(None, description="Maximum transaction amount"),
    sort_by: Optional[str] = Query("date", description="Sort by: date or amount"),
    order: Optional[str] = Query("desc", description="Order: asc or desc"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Get transactions with filters and sorting.
    - Filter by date range, category, amount range
    - Sort by date or amount (asc/desc)
    """

    query = db.query(Transaction).filter(Transaction.user_id == UUID(current_user))

    # Date filters
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    # Category filter
    if category_ids:
        query = query.join(Transaction.categories).filter(Category.id.in_(category_ids))

    # Amount range
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    # Sorting
    if sort_by == "amount":
        sort_column = Transaction.amount
    else:
        sort_column = Transaction.date

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    transactions = query.all()
    return transactions
