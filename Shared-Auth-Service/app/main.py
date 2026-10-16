from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import apps, auth
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.api.apps import ensure_default_apps


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_default_apps(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="STEM-Lab Shared Auth Service (IAM)",
    version="1.1.0",
    description="Central identity for STEM practice layers + Financial Engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(apps.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "service": "Shared-Auth-Service", "mode": "demo-sqlite"}
