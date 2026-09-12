import uuid
import enum
from sqlalchemy import Column, String, Numeric, ForeignKey, Enum, text, TIMESTAMP, Table
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class TransactionType(enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"

# Clasificadores principales
class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)

# Etiquetas transversales (Ej. "Viaje a Cancún")
class Tag(Base):
    __tablename__ = "tags"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)

# Tabla intermedia Many-to-Many para Transacciones y Etiquetas
transaction_tags = Table(
    "transaction_tags",
    Base.metadata,
    Column("transaction_id", UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

# El núcleo del movimiento de dinero
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True)
    transaction_date = Column(TIMESTAMP, server_default=text('now()'))