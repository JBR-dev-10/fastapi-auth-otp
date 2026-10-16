import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailService:
    """Servicio de correo intercambiable para el envío de notificaciones mediante Brevo (SMTP)."""
    
    @staticmethod
    def send_otp_email(to_email: str, otp_code: str):
        """Envía el código OTP de 6 dígitos al correo electrónico del usuario."""
        if not settings.BREVO_SMTP_USER or not settings.BREVO_SMTP_PASSWORD:
            # Modo desarrollo / pruebas: simula el envío imprimiendo en consola de forma segura
            print(f"[DEV EMAIL] OTP para {to_email}: {otp_code}")
            return True

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Código de Verificación OTP - Secure Auth"
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        html_content = f"""
        <html>
          <body>
            <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
              <h2>Verificación de Cuenta</h2>
              <p>Has solicitado iniciar registro o verificación en nuestra plataforma.</p>
              <p>Tu código OTP de 6 dígitos es:</p>
              <h1 style="color: #4F46E5; letter-spacing: 4px;">{otp_code}</h1>
              <p>Este código es válido por 15 minutos. Si no solicitaste este código, ignora este mensaje.</p>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP(settings.BREVO_SMTP_SERVER, settings.BREVO_SMTP_PORT) as server:
                server.starttls()
                server.login(settings.BREVO_SMTP_USER, settings.BREVO_SMTP_PASSWORD)
                server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())
            return True
        except Exception as e:
            # Se captura la excepción sin exponer detalles sensibles en los logs de error del cliente
            print(f"Error enviando correo: {str(e)}")
            return False