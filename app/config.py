from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación usando Pydantic Settings.
    Carga las variables de entorno desde el archivo .env o el entorno del sistema.
    """
    SECRET_KEY: str = "super_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DATABASE_URL: str = "sqlite:///./auth_app.db"
    
    BREVO_SMTP_SERVER: str = "smtp-relay.brevo.com"
    BREVO_SMTP_PORT: int = 587
    BREVO_SMTP_USER: str = ""
    BREVO_SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "no-reply@example.com"
    EMAILS_FROM_NAME: str = "Auth System"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()