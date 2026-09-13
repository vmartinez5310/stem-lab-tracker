import uuid
from datetime import date
from sqlalchemy.orm import Session
from app.models.finance_planning import BudgetPlan

class BudgetEngine:
    def __init__(self, db: Session):
        self.db = db

    def apply_50_30_20_rule(self, user_id: uuid.UUID, income_amount: float, target_month: date):
        needs_limit = income_amount * 0.50
        wants_limit = income_amount * 0.30
        savings_limit = income_amount * 0.20

        # Verifica si ya existe un presupuesto maestro para este mes
        plan = self.db.query(BudgetPlan).filter(
            BudgetPlan.user_id == user_id,
            BudgetPlan.month == target_month
        ).first()

        if not plan:
            plan = BudgetPlan(
                user_id=user_id,
                month=target_month,
                total_limit=income_amount
            )
            self.db.add(plan)
            # flush() envía el SQL a PostgreSQL para generar el UUID, 
            # pero NO hace el commit final, permitiendo revertir si algo falla después.
            self.db.flush() 
        else:
            plan.total_limit = float(plan.total_limit) + income_amount
            self.db.flush()

        return {
            "budget_plan_id": plan.id,
            "new_total_limit": plan.total_limit,
            "distribution": {
                "NEEDS_50": needs_limit,
                "WANTS_30": wants_limit,
                "SAVINGS_20": savings_limit
            }
        }