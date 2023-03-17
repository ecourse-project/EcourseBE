from django.apps import AppConfig


class UploadConfig(AppConfig):
    name = 'apps.upload'

    def ready(self):
        from . import signals
