from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Pydantic buscará estas variables exactas en tu archivo .env
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str

    class Config:
        # Aquí le decimos dónde está el archivo de secretos
        env_file = ".env"

# Creamos una instancia para importar 'settings' en otros archivos
settings = Settings()