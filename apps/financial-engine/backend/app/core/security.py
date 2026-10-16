"""JWT validation against the Shared-Auth-Service secret."""
from typing import Optional
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings

ALGORITHM = "HS256"
bearer_scheme = HTTPBearer(auto_error=False)


def decode_shared_token(token: str) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return payload


def get_current_user_claims(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    settings = get_settings()
    if creds is None or not creds.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_shared_token(creds.credentials)

    apps = payload.get("apps") or []
    if settings.app_slug not in apps and "admin" not in apps:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No access to '{settings.app_slug}'. Ask an admin to grant the role.",
        )

    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Token missing subject")

    return payload


def get_user_id(claims: dict = Depends(get_current_user_claims)) -> UUID:
    return UUID(str(claims["sub"]))
