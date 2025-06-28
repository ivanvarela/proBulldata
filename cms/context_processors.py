from cms.models import News


def global_params(request):
    """
    Context processor que proporciona parámetros globales para todos los templates
    """
    try:
        latest_news = News.objects.order_by('-created_at')[:20]

        return {
            'site_logo': '',
            'site_favicon': '',
            'site_name': 'bulldata',
            'contact_email': 'contacto@misitio.com',
            'social_media': {
                'facebook': '',
                'twitter': '',
                'instagram': '',
            },
            'footer_text': '© 2024 bulldata.info Todos los derechos reservados.',
            'latest_news': latest_news,
            # Añade aquí cualquier otro parámetro global que necesites
        }

    except Exception as e:
        #Fallback en caso de error
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
            'latest_news': [],
        }
