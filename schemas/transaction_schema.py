from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict, PositiveFloat, StringConstraints
from typing import Annotated


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


# Sample Categories
class CategoryType(str, Enum):
    grocery = "grocery"
    stationary = "stationary"
    accessory = "accessory"
    travel = "travel"
    shopping = "shopping"
    job = "job"


class TransactionCreate(BaseModel):
    amount: PositiveFloat
    type: TransactionType
    category: CategoryType
    description: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    date: date

    model_config = ConfigDict(extra="forbid")


class TransactionResponse(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TransactionSummary(BaseModel):
    total_income: float
    total_expenses: float
    balance: float


class MonthlyExpenses(BaseModel):
    start_date: date
    end_date: date
    total_expense: float


class CategoryWiseExpenses(BaseModel):
    category: str
    total_expense: float