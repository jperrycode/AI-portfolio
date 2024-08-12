from django.apps import AppConfig


class UseraccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.useraccount'

    def ready(self):
        import apps.useraccount.signals