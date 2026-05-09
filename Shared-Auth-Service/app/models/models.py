import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=text('now()'))
    last_login = Column(TIMESTAMP, nullable=True)

class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String(100), unique=True, nullable=False)
    api_key_hash = Column(String(255), nullable=False)
    status = Column(String(20), default='active')

class UserAppRole(Base):
    __tablename__ = "user_app_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    app_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), primary_key=True)
    role = Column(String(50), nullable=False)
    assigned_at = Column(TIMESTAMP, server_default=text('now()'))