from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserProfileUpdate
from app.security import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Retorna el perfil del usuario autenticado actual."""
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    profile_in: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza la información del perfil del usuario autenticado."""
    if profile_in.full_name is not None:
        current_user.full_name = profile_in.full_name
    if profile_in.password is not None:
        current_user.password_hash = hash_password(profile_in.password)
        
    db.commit()
    db.refresh(current_user)
    return current_user