from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, model_validator

class UserCreate(BaseModel):
    """Esquema para el registro de nuevos usuarios."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")
    password_confirmation: str
    full_name: str = Field(..., min_length=2)

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreate':
        """Valida que password y password_confirmation coincidan."""
        if self.password != self.password_confirmation:
            raise ValueError('Las contraseñas no coinciden')
        return self

class UserLogin(BaseModel):
    """Esquema para el inicio de sesión con usuario y contraseña en un único JSON."""
    email: EmailStr
    password: str

class OtpVerify(BaseModel):
    """Esquema para la verificación del código OTP."""
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)

class OtpResend(BaseModel):
    """Esquema para solicitar el reenvío del OTP."""
    email: EmailStr

class TokenRefresh(BaseModel):
    """Esquema para refrescar el token de acceso."""
    refresh_token: str

class TokenResponse(BaseModel):
    """Esquema de respuesta exitosa con tokens JWT."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserProfileUpdate(BaseModel):
    """Esquema para actualizar el perfil del usuario."""
    full_name: str | None = Field(None, min_length=2)
    password: str | None = Field(None, min_length=8)

class UserResponse(BaseModel):
    """Esquema de salida con la información pública del usuario."""
    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True