from datetime import datetime

def get_base_template(content, email=None, button_text=None, button_url=None):
    """
    Genera una plantilla HTML base para todos los correos electrónicos

    Args:
        content (str): Contenido HTML que irá en el cuerpo del correo
        email (str, optional): Email del usuario
        button_text (str, optional): Texto del botón de acción
        button_url (str, optional): URL del botón de acción

    Returns:
        str: Plantilla HTML completa formateada
    """
    current_year = datetime.now().year

    # Generar sección de botón solo si ambos parámetros están presentes
    button_section = ""
    if button_text and button_url:
        button_section = f"""
        <tr>
            <td style="padding-bottom: 30px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                    <tr>
                        <td style="border-radius: 4px; background-color: #1f2937; text-align: center;">
                            <a href="{button_url}" target="_blank" style="display: inline-block; padding: 16px 36px; font-size: 16px; color: #ffffff; text-decoration: none; border-radius: 4px; font-weight: bold;">{button_text}</a>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        """

    # Generar sección de email solo si está presente
    email_section = ""
    if email:
        email_section = f"""
        <tr>
            <td style="padding-bottom: 20px;">
                <p style="margin: 0; font-size: 16px; line-height: 24px;">
                    <strong>Correo electrónico:</strong> {email}
                </p>
            </td>
        </tr>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bulldata Dashboard</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; color: #333333; background-color: #f5f5f5;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td style="padding: 20px 0; text-align: center; background-color: #ffffff;">
                    <img src="https://bulldata.info/static/assets/img/icons/logo.png" alt="Bulldata Logo" width="120" style="display: block; margin: 0 auto;">
                </td>
            </tr>
            <tr>
                <td style="padding: 40px 30px; background-color: #ffffff;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                        {content}
                        {email_section}
                        {button_section}
                        <tr>
                            <td>
                                <p style="margin: 0; font-size: 16px; line-height: 24px;">
                                    Gracias por elegir Bulldata Analytics,<br>
                                    El equipo de Bulldata
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px 30px; text-align: center; background-color: #f5f5f5;">
                    <p style="margin: 0; font-size: 14px; color: #777777;">
                        &copy; {current_year} Bulldata Analytics. Todos los derechos reservados.
                    </p>
                    <p style="margin: 10px 0 0; font-size: 14px; color: #777777;">
                        Este es un mensaje automático, por favor no responda directamente a este correo.
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    return html_template


def get_account_approved_template(email):
    """
    Genera una plantilla HTML para notificar la aprobación de cuenta

    Args:
        email (str): Email del usuario

    Returns:
        str: Plantilla HTML formateada
    """
    content = """
    <tr>
        <td style="padding-bottom: 20px;">
            <h1 style="margin: 0; font-size: 24px; line-height: 30px; font-weight: bold; color: #333333;">¡Tu Cuenta Ha Sido Aprobada!</h1>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Estimado Usuario,
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Nos complace informarte que tu cuenta de Bulldata Dashboard ha sido aprobada. Ahora tienes acceso completo a nuestra plataforma de análisis.
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 30px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Ya puedes iniciar sesión en tu cuenta y comenzar a explorar nuestras potentes herramientas de análisis. Si tienes alguna pregunta o necesitas asistencia, no dudes en contactar a nuestro equipo de soporte.
            </p>
        </td>
    </tr>
    """

    return get_base_template(
        content=content,
        email=email,
        button_text="Iniciar Sesión en Dashboard",
        button_url="https://progra.bulldata.info"
    )


def get_password_reset_template(email, reset_url):
    """
    Genera una plantilla HTML para reseteo de contraseña

    Args:
        email (str): Email del usuario
        reset_url (str): URL para resetear la contraseña

    Returns:
        str: Plantilla HTML formateada
    """
    content = """
    <tr>
        <td style="padding-bottom: 20px;">
            <h1 style="margin: 0; font-size: 24px; line-height: 30px; font-weight: bold; color: #333333;">Solicitud de Restablecimiento de Contraseña</h1>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Estimado Usuario,
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Bulldata Dashboard. Si no realizaste esta solicitud, puedes ignorar este mensaje con seguridad.
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Tu nombre de usuario es: <strong>{{ user.username }}</strong>
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 30px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Para restablecer tu contraseña, haz clic en el botón a continuación. Este enlace caducará en 24 horas por motivos de seguridad.
            </p>
        </td>
    </tr>
    """

    return get_base_template(
        content=content,
        email=email,
        button_text="Restablecer Contraseña",
        button_url=reset_url
    )


def get_account_verification_template(email, verification_url):
    """
    Genera una plantilla HTML para verificación de cuenta

    Args:
        email (str): Email del usuario
        verification_url (str): URL para verificar la cuenta

    Returns:
        str: Plantilla HTML formateada
    """
    content = """
    <tr>
        <td style="padding-bottom: 20px;">
            <h1 style="margin: 0; font-size: 24px; line-height: 30px; font-weight: bold; color: #333333;">Verifica tu Dirección de Correo</h1>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Estimado Usuario,
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Gracias por registrarte en Bulldata Dashboard. Para completar tu registro y acceder a nuestra plataforma de análisis, por favor verifica tu dirección de correo electrónico.
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 30px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Haz clic en el botón a continuación para verificar tu dirección de correo. Si no creaste esta cuenta, puedes ignorar este mensaje con seguridad.
            </p>
        </td>
    </tr>
    """

    return get_base_template(
        content=content,
        email=email,
        button_text="Verificar Correo Electrónico",
        button_url=verification_url
    )


def get_welcome_template(email):
    """
    Genera una plantilla HTML de bienvenida después de la verificación

    Args:
        email (str): Email del usuario

    Returns:
        str: Plantilla HTML formateada
    """
    content = """
    <tr>
        <td style="padding-bottom: 20px;">
            <h1 style="margin: 0; font-size: 24px; line-height: 30px; font-weight: bold; color: #333333;">¡Bienvenido a Bulldata Dashboard!</h1>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Estimado Usuario,
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 20px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Gracias por verificar tu dirección de correo electrónico. Tu cuenta ha sido creada correctamente y está pendiente de aprobación por nuestros administradores.
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding-bottom: 30px;">
            <p style="margin: 0; font-size: 16px; line-height: 24px;">
                Recibirás otro correo electrónico una vez que tu cuenta haya sido aprobada. Este proceso suele tardar de 1 a 2 días hábiles. Si tienes alguna pregunta mientras tanto, por favor contacta a nuestro equipo de soporte.
            </p>
        </td>
    </tr>
    """

    return get_base_template(
        content=content,
        email=email,
        button_text=None,
        button_url=None
    )
