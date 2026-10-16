from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.models import User, LoginSession, OtpCode
from app.schemas import UserCreate, UserLogin, OtpVerify, OtpResend, TokenRefresh, TokenResponse, UserResponse
from app.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.services.otp_service import OtpService
from app.limiter import limiter
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario y envía automáticamente el código OTP de verificación por correo."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado"
        )
    
    new_user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        full_name=user_in.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generar y enviar OTP inicial
    OtpService.generate_and_send_otp(db, new_user.id, new_user.email)
    
    return new_user

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def verify_otp(request: Request, payload: OtpVerify, db: Session = Depends(get_db)):
    """Verifica el código OTP enviado al correo del usuario."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    success = OtpService.verify_otp(db, user.id, payload.code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código OTP inválido, expirado o ya utilizado"
        )
    
    return {"message": "Correo verificado exitosamente"}

@router.post("/resend-otp", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def resend_otp(request: Request, payload: OtpResend, db: Session = Depends(get_db)):
    """Reenvía un nuevo código OTP al correo electrónico."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    OtpService.generate_and_send_otp(db, user.id, user.email)
    return {"message": "Nuevo código OTP enviado exitosamente"}

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """Inicia sesión con credenciales en JSON y emite tokens JWT de acceso y refresco."""
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar si el usuario ha completado al menos un OTP válido o registrado
    # (Opcional: exigir OTP verificado si aplica, aquí implementamos flujo estándar)
    
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    
    # Registrar sesión activa
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_session = LoginSession(user_id=user.id, token=access_token, expires_at=expires_at)
    db.add(db_session)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: TokenRefresh, db: Session = Depends(get_db)):
    """Emite un nuevo token de acceso a partir de un refresh token válido."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de refresco inválido o expirado"
    )
    try:
        jwt_payload = jwt.decode(payload.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if jwt_payload.get("type") != "refresh":
            raise credentials_exception
        email: str = jwt_payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    access_token = create_access_token({"sub": user.email})
    
    # Registrar nueva sesión
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_session = LoginSession(user_id=user.id, token=access_token, expires_at=expires_at)
    db.add(db_session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": payload.refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, db: Session = Depends(get_db)):
    """Cierra la sesión actual revocando el token de acceso."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token no proporcionado")
    
    token = auth_header.split(" ")[1]
    session_record = db.query(LoginSession).filter(LoginSession.token == token).first()
    if session_record:
        db.delete(session_record)
        db.commit()
        
    return {"message": "Sesión cerrada exitosamente"}