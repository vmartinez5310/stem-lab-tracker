from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_payload
from app.models.models import Application, User, UserAppRole
from app.models.schemas import ApplicationCreate, ApplicationOut, GrantRoleRequest

router = APIRouter(prefix="/apps", tags=["Applications"])

DEFAULT_APPS = [
    ("science", "Science Lab", "science", "Practice modules for Science"),
    ("technology", "Technology Lab", "technology", "Practice modules for Technology"),
    ("engineering", "Engineering Lab", "engineering", "Practice modules for Engineering"),
    ("mathematics", "Mathematics Lab", "mathematics", "Practice modules for Mathematics"),
    ("financial-engine", "Financial Engine", "finance", "Personal finance & financial literacy"),
]


def ensure_default_apps(db: Session) -> None:
    for app_name, display, layer, desc in DEFAULT_APPS:
        exists = db.query(Application).filter(Application.app_name == app_name).first()
        if not exists:
            db.add(Application(app_name=app_name, display_name=display, layer=layer, description=desc))
    db.commit()


@router.get("", response_model=List[ApplicationOut])
def list_apps(db: Annotated[Session, Depends(get_db)]):
    ensure_default_apps(db)
    return db.query(Application).filter(Application.status == "active").all()


@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def register_app(payload: ApplicationCreate, db: Annotated[Session, Depends(get_db)]):
    if db.query(Application).filter(Application.app_name == payload.app_name).first():
        raise HTTPException(status_code=400, detail="App name already exists")
    app = Application(**payload.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.post("/grant-role", status_code=status.HTTP_201_CREATED)
def grant_role(body: GrantRoleRequest, db: Annotated[Session, Depends(get_db)]):
    """Demo: no auth required so first user can bootstrap access."""
    user = db.query(User).filter(User.email == body.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    app = db.query(Application).filter(Application.app_name == body.app_name).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    existing = (
        db.query(UserAppRole)
        .filter(UserAppRole.user_id == user.id, UserAppRole.app_id == app.id)
        .first()
    )
    if existing:
        existing.role = body.role
    else:
        db.add(UserAppRole(user_id=user.id, app_id=app.id, role=body.role))
    db.commit()
    return {"message": f"Granted role '{body.role}' on '{body.app_name}' to {body.user_email}"}
