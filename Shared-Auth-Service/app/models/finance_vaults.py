import uuid
import enum
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Enum, text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

# Enums para normalizar los datos en PostgreSQL
class InstitutionType(enum.Enum):
    BANK = "BANK"
    SOFIPO = "SOFIPO"
    CRYPTO = "CRYPTO"

class AccountType(enum.Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    INVESTMENT = "INVESTMENT"

class PaymentMethodType(enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    CASH = "CASH"

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
    # Vinculación estricta a tu módulo IAM centralizado
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    balance = Column(Numeric(12, 2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=text('now()'))

# Reglas de los plásticos y ciclos de crédito
class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    alias = Column(String(50), nullable=False)
    type = Column(Enum(PaymentMethodType), nullable=False)
    credit_limit = Column(Numeric(12, 2), nullable=True)
    cut_off_day = Column(Integer, nullable=True)
    due_day = Column(Integer, nullable=True)