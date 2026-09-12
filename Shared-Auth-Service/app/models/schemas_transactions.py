from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"

class TransactionCreate(BaseModel):
    user_id: UUID
    account_id: UUID
    category_id: Optional[UUID] = None
    type: TransactionType
    amount: float
    description: Optional[str] = None