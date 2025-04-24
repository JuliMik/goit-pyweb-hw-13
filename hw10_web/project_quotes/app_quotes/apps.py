from django.apps import AppConfig


# Клас конфігурації для додатку "app_quotes", що дозволяє Django налаштовувати цей додаток
class AppQuotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_quotes'
