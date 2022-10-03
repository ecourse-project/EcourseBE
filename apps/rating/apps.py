from django.apps import AppConfig


class RatingConfig(AppConfig):
    name = 'apps.rating'

    def ready(self):
        from . import signals  # noqa
