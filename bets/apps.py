from django.apps import AppConfig


class BetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bets'

    def ready(self):
        # Importar y registrar templatetags
        import bets.templatetags
