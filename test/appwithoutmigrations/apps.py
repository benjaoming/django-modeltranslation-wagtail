from django.apps import AppConfig


class AppwithoutmigrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appwithoutmigrations'
