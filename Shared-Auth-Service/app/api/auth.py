from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.models.schemas import UserCreate, UserResponse, TokenResponse
from app.core.security import create_access_token
from app.core.redis_service import generate_otp, verify_otp

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

# 1. El usuario pide su código OTP (Aquí enviaríamos el correo en el futuro)
@router.post("/request-otp")
def request_otp(email: str, db: Session = Depends(get_db)):
    # Verificar que el email esté registrado
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email no registrado")
    
    # Generar y guardar OTP en Redis
    otp = generate_otp(email)
    
    # POR AHORA: Lo devolvemos en la respuesta para poder probar
    # EN PRODUCCIÓN: Esto se envía por email y aquí solo devolvemos "Correo enviado"
    return {"message": "Código enviado", "dev_otp": otp}

# 2. El usuario entrega el código y SI ES CORRECTO, le damos un token JWT
@router.post("/verify-otp", response_model=TokenResponse)
def verify_login_otp(email: str, otp: str, db: Session = Depends(get_db)):
    if not verify_otp(email, otp):
        raise HTTPException(status_code=400, detail="Código inválido o expirado")
    
    db_user = db.query(User).filter(User.email == email).first()
    
    token_data = {"sub": str(db_user.id), "email": db_user.email}
    access_token = create_access_token(data=token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}