from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from database_models import Transaction
from schemas.transaction_schema import (
    TransactionCreate,
    TransactionResponse,
    TransactionType,
    CategoryType,
    TransactionSummary,
    CategoryWiseExpenses,
    MonthlyExpenses,
)
from datetime import date
from dependencies import required_roles
from database_models import User


router = APIRouter(prefix="/transactions", tags=["Transactions"])


# Get all Transactions
@router.get("/", response_model=list[TransactionResponse], summary= "Get All Transactions", description="Accessible by Viewers, Analysts, and Admins.")
def get_all_transactions(
    min_amount: Optional[float] = Query(None, description= "Filter by Min Price"), 
    max_amount: Optional[float] = Query(None, description= "Filter by Max Price"),
    transaction_type: Optional[TransactionType] = Query(None, description= "Select transaction type"), 
    category: Optional[CategoryType] = Query(None, description= "Select Category"), 
    date: Optional[date] = Query(None, description= "Filter by transaction date (YYYY-MM-DD)", ), 
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["viewer", "analyst", "admin"]))
): 
    
    query = db.query(Transaction)
    
    # Filter transactions by price range, type, category and date
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(status_code=400, detail="min_amount cannot be greater than max_amount")

    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
        
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type.value)
    
    if category:
        query = query.filter(Transaction.category == category.value)

    if date:
        query = query.filter(Transaction.date == date)
    
    transactions = query.all()
    if not transactions:
        raise HTTPException(status_code=404, detail= "No transactions found")
    
    return transactions


# Get recent Transactions
@router.get("/recent", response_model= List[TransactionResponse], summary= "Get Recent Transactions", description="Accessible by Viewers, Analysts, and Admins.")
def recent_transaction(
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["viewer", "analyst", "admin"]))
):
    transactions = (
        db.query(Transaction)
        .order_by(Transaction.date.desc())
        .limit(5) 
        .all()
    )
    return transactions


# Get summary of total income, total expenses and current balance
@router.get("/summary", response_model= TransactionSummary, summary= "Get Financial Summary", description="Accessible by Viewers, Analysts, and Admins.")
def summary(
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["viewer", "analyst", "admin"]))
):
    total_income = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.type == "income")
        .scalar() or 0
    )
    total_expenses = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.type == "expense")
        .scalar() or 0
    )
    balance = total_income - total_expenses
    
    return {"total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance
    }


# Get Monthly Expense Summary
@router.get("/monthly-expense", response_model=MonthlyExpenses, summary= "Get Monthly Expense Summary", description="Accessible by Viewers, Analysts, and Admins.")
def monthly_expense(
    start_date: date, 
    end_date: date, 
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["viewer", "analyst", "admin"]))
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400, 
            detail= "Start date cannot be greater than end date. Please enter valid date."
        )
    
    monthly_total_expense = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.type == "expense")
        .filter(Transaction.date >= start_date)
        .filter(Transaction.date <= end_date)
        .scalar() or 0
    )

    return {
        "start_date": start_date,        
        "end_date": end_date,
        "total_expense": monthly_total_expense
    }


# Get Category-wise Expense Summary
@router.get("/category-wise-breakdown", response_model= list[CategoryWiseExpenses], summary= "Get Category-wise Expenses", description="Accessible by Analysts and Admins.")
def category_wise_expenses(
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["analyst", "admin"]))
):
    result = (
        db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("Total Expense")
        )
        .filter(Transaction.type == "expense")
        .group_by(Transaction.category)
        .all()
    )

    return [
        {"category": category, "total_expense": total_expenses}
        for category, total_expenses in result
    ]


# Get Transaction by ID
@router.get("/{transaction_id}", response_model=TransactionResponse, summary= "Get Transaction by ID", description="Accessible by Viewers, Analysts, and Admins.")
def get_transaction_id(
    transaction_id: int, db: Session = Depends(get_db),
    user: User = Depends(required_roles(["viewer", "analyst", "admin"]))
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


# Create a new Transaction
@router.post("/", response_model=TransactionResponse, summary= "Create a Transaction", description="Accessible by Admins Only.")
def add_transaction(
    transaction: TransactionCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(required_roles(["admin"]))
):
    new_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type.value,
        category=transaction.category.value,
        description=transaction.description,
        date=transaction.date,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


# Update a Transaction
@router.put("/{transaction_id}", response_model=TransactionResponse, summary= "Update a Transaction", description="Accessible by Admins Only.")
def update_transaction(
    transaction_id: int, updated_data: TransactionCreate, 
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["admin"]))
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    transaction.amount = updated_data.amount
    transaction.type = updated_data.type.value
    transaction.category = updated_data.category.value
    transaction.description = updated_data.description
    transaction.date = updated_data.date
        
    db.commit()
    db.refresh(transaction)
    return transaction


# Delete a Transaction
@router.delete("/{transaction_id}", summary= "Delete a Transaction", description="Accessible by Admins Only.")
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(required_roles(["admin"]))
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
