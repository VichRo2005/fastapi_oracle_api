from email.message import EmailMessage
import smtplib
from app.core.config import settings  # Asegúrate de tener tus settings bien cargados

def enviar_codigo_verificacion(destinatario: str, codigo: str):
    msg = EmailMessage()
    msg['Subject'] = 'Código de verificación - Recuperación de contraseña'
    msg['From'] = settings.MAIL_USER
    msg['To'] = destinatario

    msg.set_content(f"""
    Estimado/a,

    Ha solicitado restablecer su contraseña. Utilice el siguiente código de verificación para continuar con el proceso:

    Código de verificación: {codigo}

    Este código es válido solo por 5 minutos.

    Si no solicitó este cambio, ignore este mensaje.

    Saludos,
    Equipo Ferremas
    """)

    with smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USER, settings.MAIL_PASSWORD)
        server.send_message(msg)
