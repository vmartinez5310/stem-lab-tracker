from app.core.database import SessionLocal
# Ajusta "auth" si guardaste la clase User en otro archivo (ej. models.py)
from app.models.models import User
from app.models.finance_vaults import Institution, InstitutionType, Account, AccountType
from app.models.finance_transactions import Category, TransactionType

db = SessionLocal()

# 1. Inyectar Usuario
user = User(email="ingeniero+QA1@stemlab.com", phone_number="5551234568")
db.add(user)
db.commit()
db.refresh(user)

# 2. Inyectar Institución
inst = Institution(name="BBVA", type=InstitutionType.BANK)
db.add(inst)
db.commit()
db.refresh(inst)

# 3. Inyectar Cuenta (Bóveda)
account = Account(user_id=user.id, institution_id=inst.id, name="Débito Nómina", type=AccountType.CHECKING, balance=15000.00)
db.add(account)
db.commit()
db.refresh(account)

# 4. Inyectar Categoría de Gasto
category = Category(user_id=user.id, name="Servicios Web", type=TransactionType.EXPENSE)
db.add(category)
db.commit()
db.refresh(category)

print("--- COPIA ESTOS UUIDS PARA SWAGGER ---")
print(f"user_id: {user.id}")
print(f"account_id: {account.id}")
print(f"category_id: {category.id}")