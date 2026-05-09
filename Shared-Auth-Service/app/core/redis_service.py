import redis
import random
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def generate_otp(email: str) -> str:
    # Generamos un c`ódigo OTP de 6 dígitos `
    otp = f"{random.randint(100000, 999999)}"

    # Lo guardamos en Redis: clave = email, valor = otp
    # ex=300 significa que expira en 5 minutos (300 segundos)
    redis_client.set(name=f"otp:{email}", value=otp, ex=300)

    return otp

def verify_otp(email: str, otp: str):
    #Buscamos el código guardado
    stored_otp = redis_client.get(name=f"otp:{email}")

    #Si existe y coincide, es válido
    if stored_otp and stored_otp == otp:
        redis_client.delete(f"otp:{email}")  # Eliminamos el OTP después de usarlo
        return True
    return False
