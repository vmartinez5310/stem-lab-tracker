# STEM-Lab Tracker & Modular Ecosystem

Monorepo with **centralized IAM (Shared-Auth-Service)** and modular applications.

One identity → many STEM practice layers + **Financial Engine** (financial literacy / personal finance module).

---

## Architecture

```text
┌────────────────────────────────────────────────────────────────┐
│                    Shared-Auth-Service (IAM)                   │
│  Users · Applications · UserAppRoles · OTP · JWT               │
│  Port 8001                                                     │
└──────────────────────────────┬─────────────────────────────────┘
                               │ JWT (sub=user_uuid, email, apps)
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
      Science App        Technology App     Financial Engine
      (future)           (future)           Port 8000 + 5173
```

### Multi-layer OAuth model

| Entity         | Purpose                                              |
|----------------|------------------------------------------------------|
| `User`         | Single identity (UUID, email, phone)                 |
| `Application`  | Registered app (science, technology, engineering, mathematics, **financial-engine**) |
| `UserAppRole`  | Grants a user a role inside a specific application   |

A user authenticates **once** via OTP. The JWT can carry the list of apps they can access. Each app validates the token and checks its own role.

---

## Apps in this monorepo

| Path                         | Description                                      |
|------------------------------|--------------------------------------------------|
| `Shared-Auth-Service/`       | Central IAM (OTP + JWT + app registry)           |
| `apps/financial-engine/`     | Personal finance / financial-literacy module     |

Future STEM layers can live under `apps/science`, `apps/technology`, etc., all consuming the same IAM.

---

## Quick start

```bash
# 1. Infrastructure (Postgres + Redis)
docker compose up -d db redis

# 2. Shared Auth
cd Shared-Auth-Service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8001

# 3. Financial Engine backend
cd ../apps/financial-engine/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# 4. Financial Engine frontend
cd ../frontend
npm install && npm run dev
```

See `docs/INTEGRATION.md` for the full auth contract and how to register new STEM apps.

---

## Auth flow (all apps)

1. `POST /auth/register` → create user in IAM  
2. `POST /auth/request-otp` → OTP stored in Redis (dev returns the code)  
3. `POST /auth/verify-otp` → JWT  
4. Client sends `Authorization: Bearer <jwt>` to any app  
5. App validates JWT with the **shared SECRET_KEY** and checks `UserAppRole` for its `app_name`

Financial Engine no longer has its own password auth; it trusts the Shared-Auth-Service.
