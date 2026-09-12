import uuid
import enum
from sqlalchemy import Column, String, Numeric, ForeignKey, Enum, text, TIMESTAMP, Date
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class GoalStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"

class IOUDirection(enum.Enum):
    I_OWE = "I_OWE"
    THEY_OWE = "THEY_OWE"

# Presupuestos Mensuales
class BudgetPlan(Base):
    __tablename__ = "budget_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    month = Column(Date, nullable=False) # Ej. 2026-10-01
    total_limit = Column(Numeric(12, 2), nullable=False)

class BudgetItem(Base):
    __tablename__ = "budget_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    budget_id = Column(UUID(as_uuid=True), ForeignKey("budget_plans.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    limit_amount = Column(Numeric(12, 2), nullable=False)

# Metas de Ahorro
class SavingsGoal(Base):
    __tablename__ = "savings_goals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    target_amount = Column(Numeric(12, 2), nullable=False)
    current_amount = Column(Numeric(12, 2), default=0.00)
    status = Column(Enum(GoalStatus), default=GoalStatus.ACTIVE)
    deadline = Column(Date, nullable=True)

# Gestión de Deudas a Terceros (IOU)
class IOULedger(Base):
    __tablename__ = "iou_ledger"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    counterparty_name = Column(String(100), nullable=False)
    direction = Column(Enum(IOUDirection), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('now()'))