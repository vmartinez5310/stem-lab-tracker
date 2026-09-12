from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.finance_obligations import RecurringBill, InstallmentPlan
from app.models.schemas_obligations import RecurringBillCreate, InstallmentPlanCreate

router = APIRouter(prefix="/finance/obligations", tags=["Obligaciones Financieras"])

@router.post("/bills/")
def create_recurring_bill(bill: RecurringBillCreate, db: Session = Depends(get_db)):
    new_bill = RecurringBill(**bill.model_dump())
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill

@router.post("/installments/")
def create_installment_plan(plan: InstallmentPlanCreate, db: Session = Depends(get_db)):
    new_plan = InstallmentPlan(**plan.model_dump())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan