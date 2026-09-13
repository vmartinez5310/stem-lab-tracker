import uuid
from datetime import date
from sqlalchemy.orm import Session
from app.models.finance_planning import BudgetPlan
from app.models.finance_planning import BudgetItem
from app.models.finance_profiles import FinancialProfile
from app.models.finance_vaults import Account, AccountType

class BudgetEngine:
    def __init__(self, db: Session):
        self.db = db

    def apply_dynamic_distribution(self, user_id: uuid.UUID, income_amount: float, target_month: date):
        # 1. Consulta del perfil financiero parametrizado
        profile = self.db.query(FinancialProfile).filter(FinancialProfile.user_id == user_id).first()
        
        # 2. Asignación dinámica con fallback de seguridad
        needs_pct = float(profile.needs_pct) if profile else 0.50
        wants_pct = float(profile.wants_pct) if profile else 0.30
        savings_pct = float(profile.savings_pct) if profile else 0.20

        # 3. Matemática financiera personalizada
        needs_limit = income_amount * needs_pct
        wants_limit = income_amount * wants_pct
        savings_limit = income_amount * savings_pct

        # 4. Gestión del Presupuesto Maestro (BudgetPlan)
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
            self.db.flush() 
        else:
            plan.total_limit = float(plan.total_limit) + income_amount
            self.db.flush()

        # Retorno de la distribución exacta
        return {
            "budget_plan_id": plan.id,
            "new_total_limit": plan.total_limit,
            "distribution": {
                "NEEDS": needs_limit,
                "WANTS": wants_limit,
                "SAVINGS": savings_limit
            }
        }

    def process_expense(self, user_id: uuid.UUID, account_id: uuid.UUID, category_id: uuid.UUID, amount: float, target_month: date):
        # 1. Impacto Físico (Liquidez de la Cuenta)
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError("La cuenta especificada no existe.")

        account.current_balance = float(account.current_balance) - amount
        
        # 2. Impacto Maestro (Presupuesto Mensual Total)
        plan = self.db.query(BudgetPlan).filter(
            BudgetPlan.user_id == user_id,
            BudgetPlan.month == target_month
        ).first()

        plan_status = None
        category_status = None

        if plan:
            plan.total_consumed = float(getattr(plan, 'total_consumed', 0.0)) + amount
            plan_status = {
                "budget_plan_id": plan.id,
                "total_consumed": plan.total_consumed,
                "remaining_budget": float(plan.total_limit) - plan.total_consumed
            }

            # 3. Impacto Específico (Cubeta de la Categoría)
            if category_id:
                budget_item = self.db.query(BudgetItem).filter(
                    BudgetItem.budget_id == plan.id,
                    BudgetItem.category_id == category_id
                ).first()

                if budget_item:
                    budget_item.consumed_amount = float(getattr(budget_item, 'consumed_amount', 0.0)) + amount
                    category_status = {
                        "category_id": category_id,
                        "consumed": budget_item.consumed_amount,
                        "limit": budget_item.limit_amount,
                        "remaining_in_category": float(budget_item.limit_amount) - budget_item.consumed_amount
                    }

        self.db.flush()
        is_overdrawn = account.current_balance < 0 and account.account_type in [AccountType.DEBIT, AccountType.CASH]

        return {
            "liquidity": {
                "account_id": account.id,
                "new_balance": account.current_balance,
                "is_overdrawn": is_overdrawn
            },
            "budget": plan_status,
            "category_impact": category_status
        }