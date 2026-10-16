from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user_claims, get_user_id
from app.db.session import get_db
from app.models.user import User


def get_or_create_local_user(
    db: Annotated[Session, Depends(get_db)],
    claims: Annotated[dict, Depends(get_current_user_claims)],
) -> User:
    """Ensures a local finance profile exists for the IAM user."""
    user_id = UUID(str(claims["sub"]))
    user = db.get(User, user_id)
    if user is None:
        user = User(
            id=user_id,
            email=claims.get("email") or f"{user_id}@unknown",
            full_name=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
