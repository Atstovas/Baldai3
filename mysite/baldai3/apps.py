from django.apps import AppConfig


class Baldai3Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baldai3'

    def ready(self):
        from .signals import create_profile, save_profile
