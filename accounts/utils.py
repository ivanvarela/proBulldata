from django.core.mail import EmailMessage
from utils.email_templates import (
    get_password_reset_template,
    get_account_verification_template,
    get_welcome_template
)


def send_password_reset_email(email, reset_url):
    """
    Envía un correo de restablecimiento de contraseña

    Args:
        email (str): Email del usuario
        reset_url (str): URL para resetear la contraseña

    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        subject = "Restablecer tu contraseña de Bulldata Dashboard"
        html_message = get_password_reset_template(email, reset_url)

        email_message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='noreply@bulldata.info',
            to=[email],
        )

        email_message.content_subtype = "html"
        email_message.send()
        return True

    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False


def send_verification_email(email, verification_url):
    """
    Envía un correo de verificación de cuenta

    Args:
        email (str): Email del usuario
        verification_url (str): URL para verificar la cuenta

    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        subject = "Verifica tu cuenta de Bulldata Dashboard"
        html_message = get_account_verification_template(email, verification_url)

        email_message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='noreply@bulldata.info',
            to=[email],
        )

        email_message.content_subtype = "html"
        email_message.send()
        return True

    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return False


def send_welcome_email(email):
    """
    Envía un correo de bienvenida después de la verificación

    Args:
        email (str): Email del usuario

    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        subject = "Bienvenido a Bulldata Dashboard"
        html_message = get_welcome_template(email)

        email_message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='noreply@bulldata.info',
            to=[email],
        )

        email_message.content_subtype = "html"
        email_message.send()
        return True

    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False
