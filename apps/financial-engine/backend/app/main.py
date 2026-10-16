from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import accounts, transactions
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

from app.models import user, account, transaction, category, budget, goal  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Financial Engine — STEM-Lab module (auth via Shared-Auth-Service)",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "auth": "Shared-Auth-Service",
        "app_slug": settings.app_slug,
    }
