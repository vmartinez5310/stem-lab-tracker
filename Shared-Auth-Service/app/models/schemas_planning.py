from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class BudgetPlanCreate(BaseModel):
    user_id: UUID
    month: date
    total_limit: float

class SavingsGoalCreate(BaseModel):
    user_id: UUID
    name: str
    target_amount: float
    deadline: Optional[date] = None