from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum

class AccountType(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    INVESTMENT = "INVESTMENT"

class AccountCreate(BaseModel):
    user_id: UUID
    institution_id: UUID
    name: str
    type: AccountType
    balance: Optional[float] = 0.00