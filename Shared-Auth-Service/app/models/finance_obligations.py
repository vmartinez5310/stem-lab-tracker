import uuid
import enum
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Enum, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Periodicity(enum.Enum):
    MONTHLY = "MONTHLY"
    BIMONTHLY = "BIMONTHLY"
    YEARLY = "YEARLY"

class InstallmentStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DEFAULTED = "DEFAULTED"

# Recibos Fijos (Renta, CFE, Teléfono)
class RecurringBill(Base):
    __tablename__ = "recurring_bills"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(100), nullable=False)
    expected_amount = Column(Numeric(12, 2), nullable=False)
    periodicity = Column(Enum(Periodicity), nullable=False)
    next_due_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

# Cargos Demorados y MSI (iPhone for Life, Palacio de Hierro)
class InstallmentPlan(Base):
    __tablename__ = "installment_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    monthly_amount = Column(Numeric(12, 2), nullable=False)
    residual_value = Column(Numeric(12, 2), default=0.00) # Cargo final del plan Get/For Life
    total_installments = Column(Integer, nullable=False)
    paid_installments = Column(Integer, default=0)
    start_date = Column(Date, nullable=False)
    status = Column(Enum(InstallmentStatus), default=InstallmentStatus.ACTIVE)