from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.finance_vaults import Account
from app.models.schemas_finance import AccountCreate

router = APIRouter(prefix="/finance", tags=["Bóvedas Financieras"])

@router.post("/accounts/")
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    new_account = Account(**account.model_dump())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account