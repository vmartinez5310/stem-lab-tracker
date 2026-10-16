from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_or_create_local_user
from app.db.session import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _get_owned_account(db: Session, account_id: int, user_id) -> Account:
    account = db.get(Account, account_id)
    if not account or account.user_id != user_id:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("", response_model=List[TransactionOut])
def list_transactions(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_or_create_local_user)],
    account_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> List[Transaction]:
    q = (
        db.query(Transaction)
        .join(Account)
        .filter(Account.user_id == current_user.id)
    )
    if account_id is not None:
        q = q.filter(Transaction.account_id == account_id)
    return q.order_by(Transaction.date.desc(), Transaction.id.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_or_create_local_user)],
) -> Transaction:
    account = _get_owned_account(db, payload.account_id, current_user.id)
    tx = Transaction(**payload.model_dump())
    db.add(tx)
    if payload.type == "income":
        account.balance += payload.amount
    elif payload.type == "expense":
        account.balance -= payload.amount
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_or_create_local_user)],
) -> Transaction:
    tx = (
        db.query(Transaction)
        .join(Account)
        .filter(Transaction.id == transaction_id, Account.user_id == current_user.id)
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.patch("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_or_create_local_user)],
) -> Transaction:
    tx = (
        db.query(Transaction)
        .join(Account)
        .filter(Transaction.id == transaction_id, Account.user_id == current_user.id)
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(tx, field, value)
    db.commit()
    db.refresh(tx)
    return tx


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_or_create_local_user)],
) -> None:
    tx = (
        db.query(Transaction)
        .join(Account)
        .filter(Transaction.id == transaction_id, Account.user_id == current_user.id)
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(tx)
    db.commit()
