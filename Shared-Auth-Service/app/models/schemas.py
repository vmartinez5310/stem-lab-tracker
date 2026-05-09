from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

# Lo que recibimos del Frontend
class UserCreate(BaseModel):
    email: EmailStr
    phone_number: Optional[str] = None

# Lo que respondemos al Frontend (por seguridad no devolvemos todo)
class UserResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool

    class Config:
        from_attributes = True