from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from datetime import datetime
from app.models.finance_transactions import Transaction
from app.models.schemas_transactions import TransactionCreate
from app.services.budget_engine import BudgetEngine
from app.models.finance_transactions import TransactionType 

router = APIRouter(prefix="/finance/transactions", tags=["Operativa Diaria"])

@router.post("/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # 1. Instanciar el motor analítico
    budget_engine = BudgetEngine(db)
    
   # 2. Intercepción Estratégica Corregida
    engine_result = None
    
    # Validamos tanto el objeto Enum como el string plano
    is_income = transaction.type in [TransactionType.INCOME, "INCOME", "TransactionType.INCOME"]
    
    # Leemos 'description' en lugar de 'name', asegurando que no llegue vacío
    has_salario = transaction.description and "salario" in transaction.description.lower()
    
    if is_income and has_salario:
        # El servidor calcula el mes en curso automáticamente
        target_month = date.today().replace(day=1) 
        engine_result = budget_engine.apply_50_30_20_rule(
            user_id=transaction.user_id,
            income_amount=transaction.amount,
            target_month=target_month
        )
    
    # 3. Persistencia de la Transacción Original
    new_transaction = Transaction(**transaction.model_dump())
    db.add(new_transaction)
    
    # 4. Commit Atómico (Guarda la transacción y la división 50/30/20 al mismo tiempo)
    db.commit()
    db.refresh(new_transaction)
    
    return {
        "transaction": new_transaction,
        "automation": engine_result
    }