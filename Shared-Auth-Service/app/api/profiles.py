from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.finance_profiles import FinancialProfile
from app.models.schemas_profiles import FinancialProfileUpdate
from uuid import UUID

router = APIRouter(prefix="/finance/profiles", tags=["Perfiles Financieros"])

@router.put("/{user_id}")
def update_financial_profile(user_id: UUID, profile: FinancialProfileUpdate, db: Session = Depends(get_db)):
    db_profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == user_id).first()
    
    if not db_profile:
        db_profile = FinancialProfile(
            user_id=user_id,
            needs_pct=profile.needs_pct,
            wants_pct=profile.wants_pct,
            savings_pct=profile.savings_pct
        )
        db.add(db_profile)
    else:
        db_profile.needs_pct = profile.needs_pct
        db_profile.wants_pct = profile.wants_pct
        db_profile.savings_pct = profile.savings_pct
        
    db.commit()
    db.refresh(db_profile)
    return db_profile