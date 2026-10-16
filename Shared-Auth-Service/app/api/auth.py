from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.redis_service import generate_otp, verify_otp
from app.core.security import create_access_token, get_current_payload
from app.models.models import Application, User, UserAppRole
from app.models.schemas import TokenResponse, UserCreate, UserResponse, UserAppsResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _user_app_names(db: Session, user_id) -> list[str]:
    rows = (
        db.query(Application.app_name)
        .join(UserAppRole, UserAppRole.app_id == Application.id)
        .filter(UserAppRole.user_id == user_id, Application.status == "active")
        .all()
    )
    return [r[0] for r in rows]


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]) -> User:
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_data.email,
        phone_number=user_data.phone_number,
        full_name=user_data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/request-otp")
def request_otp(email: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")
    otp = generate_otp(email)
    return {"message": "OTP sent", "dev_otp": otp}


@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp_login(
    email: str = Query(...),
    otp: str = Query(...),
    db: Session = Depends(get_db),
):
    if not verify_otp(email, otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    user.is_verified = True
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    apps = _user_app_names(db, user.id)
    token = create_access_token(user_id=user.id, email=user.email, apps=apps)
    return TokenResponse(access_token=token, apps=apps)


@router.get("/me", response_model=UserAppsResponse)
def me(
    payload: Annotated[dict, Depends(get_current_payload)],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.get(User, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    apps = _user_app_names(db, user.id)
    return UserAppsResponse(user_id=user.id, email=user.email, apps=apps)
