from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'apps.carts'

    def ready(self):
        from . import signals  # noqa

