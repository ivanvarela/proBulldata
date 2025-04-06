def global_params(request):
    """
    Context processor que proporciona parámetros globales para todos los templates
    """
    return {
        'site_logo': '',
        'site_favicon': '',
        'site_name': 'ElGuaire.com',
        'contact_email': 'contacto@misitio.com',
        'social_media': {
            'facebook': '',
            'twitter': '',
            'instagram': '',
        },
        'footer_text': '© 2024 ElGuaire.com Todos los derechos reservados.',
        # Añade aquí cualquier otro parámetro global que necesites
    }
