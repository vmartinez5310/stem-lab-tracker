from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.models.schemas import UserCreate, UserResponse, TokenResponse
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 2. Crear nuevo usuario (UUID se genera solo)
    new_user = User(
        email=user_data.email,
        phone_number=user_data.phone_number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
def login(email: str, db: Session = Depends(get_db)):
    # 1. Buscamos el usuario por su correo en la base de datos
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    
    # 2. Creamos la "Credencial" (payload) que irá dentro del token
    token_data = {
        "user_id": str(db_user.id),  # Convertimos UUID a string para el token
        "email": db_user.email
    }

    # 3. Generamos el token firmado
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}
    