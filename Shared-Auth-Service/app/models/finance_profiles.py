import uuid
from sqlalchemy import Column, Numeric, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    needs_pct = Column(Numeric(5, 4), nullable=False, default=0.50)
    wants_pct = Column(Numeric(5, 4), nullable=False, default=0.30)
    savings_pct = Column(Numeric(5, 4), nullable=False, default=0.20)
    
    updated_at = Column(TIMESTAMP, server_default=text('now()'), onupdate=text('now()'))