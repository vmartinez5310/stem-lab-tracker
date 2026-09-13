from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum

class AccountType(str, Enum):
    CASH = "CASH"
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class AccountCreate(BaseModel):
    user_id: UUID
    institution_id: UUID
    name: str
    account_type: AccountType
    current_balance: Optional[float] = 0.00
    credit_limit: Optional[float] = None
    currency_code: Optional[str] = "MXN"
    exchange_rate: Optional[float] = 1.00