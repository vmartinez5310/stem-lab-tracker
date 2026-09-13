import uuid
import enum
from sqlalchemy import Enum as SQLEnum, Numeric
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Enum, text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class AccountType(enum.Enum):
    CASH = "CASH"
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class PaymentMethodType(enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    CASH = "CASH"
class InstitutionType(enum.Enum):
    BANK = "BANK"
    SOFIPO = "SOFIPO"
    CRYPTO = "CRYPTO"
# Catálogo Maestro (Ej. Nu, BBVA)
class Institution(Base):
    __tablename__ = "institutions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    type = Column(Enum(InstitutionType), nullable=False)

# Las bóvedas donde vive el dinero
class Account(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=False)
    name = Column(String(100), nullable=False)
    account_type = Column(SQLEnum(AccountType), nullable=False, default=AccountType.DEBIT)
    current_balance = Column(Numeric(12, 2), default=0.00)
    credit_limit = Column(Numeric(12, 2), nullable=True)
    frozen_credit = Column(Numeric(12, 2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=text('now()'))
    currency_code = Column(String(3), nullable=False, default="MXN")
    exchange_rate = Column(Numeric(12, 6), nullable=False, default=1.0)

# Reglas de los plásticos y ciclos de crédito
# Actualización del Plástico
class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    alias = Column(String(50), nullable=False)
    type = Column(Enum(PaymentMethodType), nullable=False)
    credit_limit = Column(Numeric(12, 2), nullable=True)
    frozen_credit = Column(Numeric(12, 2), default=0.00) # El candado para MSI y Balloon Payments
    cut_off_day = Column(Integer, nullable=True)
    due_day = Column(Integer, nullable=True)
