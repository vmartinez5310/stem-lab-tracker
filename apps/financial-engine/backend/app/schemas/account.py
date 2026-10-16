from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    type: str = "checking"
    currency: str = "USD"
    balance: Decimal = Decimal("0")
    credit_limit: Optional[Decimal] = None
    institution: Optional[str] = None
    color: Optional[str] = None


class AccountUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    type: Optional[str] = None
    currency: Optional[str] = None
    balance: Optional[Decimal] = None
    credit_limit: Optional[Decimal] = None
    institution: Optional[str] = None
    color: Optional[str] = None
    is_archived: Optional[bool] = None


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    currency: str
    balance: Decimal
    credit_limit: Optional[Decimal] = None
    institution: Optional[str] = None
    color: Optional[str] = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
