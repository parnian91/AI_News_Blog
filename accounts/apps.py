from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# class AccountsConfig(AppConfig):
#     name = 'accounts'

    def ready(self):
        import accounts.signals  # Import signals to auto-create profiles
