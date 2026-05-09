import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

# Configuraciones de nuestro Token
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # El token durará 7 días

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Calculamos la fecha de expiración usando zonas horarias seguras
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Firmamos el token con nuestro secreto
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt