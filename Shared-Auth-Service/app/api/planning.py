from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.finance_planning import BudgetPlan, SavingsGoal
from app.models.schemas_planning import BudgetPlanCreate, SavingsGoalCreate

router = APIRouter(prefix="/finance/planning", tags=["Proyecciones y Metas"])

@router.post("/budgets/")
def create_budget(budget: BudgetPlanCreate, db: Session = Depends(get_db)):
    new_budget = BudgetPlan(**budget.model_dump())
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

@router.post("/goals/")
def create_goal(goal: SavingsGoalCreate, db: Session = Depends(get_db)):
    new_goal = SavingsGoal(**goal.model_dump())
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal