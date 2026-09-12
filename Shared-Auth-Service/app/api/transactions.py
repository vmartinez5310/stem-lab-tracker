from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.finance_transactions import Transaction
from app.models.schemas_transactions import TransactionCreate

router = APIRouter(prefix="/finance/transactions", tags=["Operativa Diaria"])

@router.post("/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    new_tx = Transaction(**transaction.model_dump())
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx