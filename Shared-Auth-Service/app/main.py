from fastapi import FastAPI
import redis
from app.core.config import settings
from app.core.database import engine, Base
from app.models.models import User, Application, UserAppRole
from app.models import finance_vaults
from app.models import finance_transactions

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shared Auth Service (IAM)")

# Conexión a Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

@app.get("/")
async def root():
    try:
        redis_status = redis_client.ping()
    except:
        redis_status = False
    return {"message": "IAM Service Online", "redis_connected": redis_status}

from app.api.auth import router as auth_router
from app.api.finance import router as finance_router
from app.api.transactions import router as transactions_router

app.include_router(auth_router)
app.include_router(finance_router)
app.include_router(transactions_router)