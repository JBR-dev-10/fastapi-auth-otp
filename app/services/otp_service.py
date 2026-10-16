import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import OtpCode
from app.services.email_service import EmailService

class OtpService:
    """Servicio para la generación, almacenamiento y validación de códigos OTP."""

    @staticmethod
    def generate_and_send_otp(db: Session, user_id: int, email: str) -> OtpCode:
        """Genera un OTP aleatorio de 6 dígitos, lo almacena con expiración de 15 min y lo envía."""
        # Invalidar OTPs anteriores no usados de este usuario
        db.query(OtpCode).filter(OtpCode.user_id == user_id, OtpCode.used == False).update({"used": True})
        
        code = f"{random.randint(0, 999999):06d}"
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        otp_record = OtpCode(
            user_id=user_id,
            code=code,
            expires_at=expires_at,
            used=False
        )
        db.add(otp_record)
        db.commit()
        db.refresh(otp_record)
        
        # Enviar correo
        EmailService.send_otp_email(email, code)
        return otp_record

    @staticmethod
    def verify_otp(db: Session, user_id: int, code: str) -> bool:
        """Verifica que el OTP sea válido, no haya expirado y no haya sido usado previamente."""
        otp_record = db.query(OtpCode).filter(
            OtpCode.user_id == user_id,
            OtpCode.code == code,
            OtpCode.used == False,
            OtpCode.expires_at > datetime.utcnow()
        ).first()

        if not otp_record:
            return False

        # Marcar como usado (un OTP usado no puede reutilizarse)
        otp_record.used = True
        db.commit()
        return True