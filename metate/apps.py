from django.apps import AppConfig


class MetateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metate'

    def ready(self):
        import metate.signals
