from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    phone_number: Optional[str] = None
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    apps: List[str] = []


class ApplicationCreate(BaseModel):
    app_name: str = Field(min_length=2, max_length=100)
    display_name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None
    layer: str = "other"


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    app_name: str
    display_name: str
    description: Optional[str] = None
    layer: str
    status: str


class GrantRoleRequest(BaseModel):
    user_email: EmailStr
    app_name: str
    role: str = "user"


class UserAppsResponse(BaseModel):
    user_id: UUID
    email: str
    apps: List[str]
