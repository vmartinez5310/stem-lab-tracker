from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.finance_transactions import TransactionType

class TransactionCreate(BaseModel):
    user_id: UUID
    account_id: UUID
    category_id: UUID
    name: Optional[str] = None
    type: TransactionType
    amount: float
    description: str
    transaction_date: Optional[datetime] = None # Nuevo campo habilitado