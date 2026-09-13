from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from datetime import date, datetime
from app.models.finance_transactions import Transaction, TransactionType
from app.models.schemas_transactions import TransactionCreate
from app.services.budget_engine import BudgetEngine

router = APIRouter(prefix="/finance/transactions", tags=["Operativa Diaria"])

@router.post("/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    budget_engine = BudgetEngine(db)
    engine_result = None
    
    # 1. Declaración explícita de banderas para evitar NameError
    is_income = transaction.type in [TransactionType.INCOME, "INCOME", "TransactionType.INCOME"]
    is_expense = transaction.type in [TransactionType.EXPENSE, "EXPENSE", "TransactionType.EXPENSE"]
    has_salario = transaction.description and "salario" in transaction.description.lower()
    
    # 2. Intercepción Estratégica
    if is_income and has_salario:
        # Prioridad de fechas consolidada en una sola evaluación
        effective_date = transaction.target_budget_month or transaction.transaction_date or datetime.now()
        target_month = effective_date.date().replace(day=1) if isinstance(effective_date, datetime) else effective_date.replace(day=1)
        
        engine_result = budget_engine.apply_dynamic_distribution(
            user_id=transaction.user_id,
            income_amount=transaction.amount,
            target_month=target_month
        )

    elif is_expense:
        # A. Identificar a qué mes de presupuesto afecta este gasto
        effective_date = transaction.target_budget_month or transaction.transaction_date or datetime.now()
        target_month = effective_date.date().replace(day=1) if isinstance(effective_date, datetime) else effective_date.replace(day=1)
        
        # B. Disparo ipso facto del doble impacto (Física y Presupuesto)
        engine_result = budget_engine.process_expense(
            user_id=transaction.user_id,
            account_id=transaction.account_id,
            category_id=transaction.category_id,
            amount=transaction.amount,
            target_month=target_month
        )
    
    # 3. Persistencia Atómica
    new_transaction = Transaction(**transaction.model_dump())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return {
        "transaction": new_transaction,
        "automation": engine_result
    }