from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Montar archivos estáticos para el frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registro de routers de API
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/", tags=["Frontend"])
def serve_frontend():
    """Sirve la interfaz web de usuario."""
    return FileResponse("app/static/index.html")

@app.get("/health", tags=["Health Check"])
def health_check():
    """Endpoint de verificación de estado del servicio."""
    return {"status": "online", "service": "Secure Auth API"}