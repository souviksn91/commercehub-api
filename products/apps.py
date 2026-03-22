from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'products'

    # ready() ensures Django activates the signal handlers when the app is ready
    def ready(self):
        import products.signals
