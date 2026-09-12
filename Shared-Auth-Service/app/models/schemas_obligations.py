from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date
from app.models.finance_obligations import Periodicity

class RecurringBillCreate(BaseModel):
    user_id: UUID
    category_id: Optional[UUID] = None
    name: str
    expected_amount: float
    periodicity: Periodicity
    next_due_date: date

class InstallmentPlanCreate(BaseModel):
    user_id: UUID
    account_id: UUID
    name: str
    total_amount: float
    monthly_amount: float
    residual_value: Optional[float] = 0.00
    total_installments: int
    start_date: date