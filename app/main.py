from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.database import engine, Base
from app.limiter import limiter
from app.routers import auth, users

# Creación automática de tablas en SQLite al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Auth System with OTP & FastAPI",
    description="Sistema completo de autenticación con FastAPI, SQLAlchemy, JWT y OTP por correo (Brevo).",
    version="1.0.0"
)

# Configuración de Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Registro de routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/", tags=["Health Check"])
def root():
    """Endpoint raíz para verificación de estado del servicio."""
    return {"status": "online", "service": "Secure Auth API"}