from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BudgetLineCreate(BaseModel):
    category_id: Optional[int] = None
    amount: Decimal = Field(gt=0)


class BudgetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    period_start: date
    period_end: date
    currency: str = "USD"
    lines: List[BudgetLineCreate] = []


class BudgetLineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: Optional[int] = None
    amount: Decimal
    spent: Decimal


class BudgetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    period_start: date
    period_end: date
    currency: str
    created_at: datetime
    lines: List[BudgetLineOut] = []
