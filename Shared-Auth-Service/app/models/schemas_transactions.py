from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from app.models.finance_transactions import TransactionType

class TransactionCreate(BaseModel):
    user_id: UUID
    account_id: UUID
    category_id: Optional[UUID] = None
    type: TransactionType
    amount: float
    description: str
    
    # Desacoplamiento temporal
    transaction_date: Optional[datetime] = None
    target_budget_month: Optional[date] = None 
    
    # RF-08: Digitalización y OCR
    receipt_url: Optional[str] = None
    attachments_data: Optional[str] = None 
    
    # RF-09: Multimoneda
    currency_code: Optional[str] = "MXN"
    exchange_rate: Optional[float] = 1.00
    
    # RF-14: Prevención de duplicados de Apple/Google Wallet
    external_sync_id: Optional[str] = Field(None, max_length=100)