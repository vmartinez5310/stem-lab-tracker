from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    type: str
    amount: Decimal = Field(gt=0)
    currency: str = "USD"
    description: Optional[str] = None
    notes: Optional[str] = None
    merchant: Optional[str] = None
    date: date
    is_recurring: bool = False


class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    type: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    currency: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[date] = None
    is_recurring: Optional[bool] = None


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    category_id: Optional[int] = None
    type: str
    amount: Decimal
    currency: str
    description: Optional[str] = None
    notes: Optional[str] = None
    merchant: Optional[str] = None
    date: date
    is_recurring: bool
    created_at: datetime
    updated_at: datetime
