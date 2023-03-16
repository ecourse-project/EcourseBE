import os

from django.db import models
from django.dispatch import receiver

from apps.upload.models import UploadFile, UploadImage


@receiver(models.signals.post_delete, sender=UploadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)


@receiver(models.signals.post_delete, sender=UploadImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image_path:
        if os.path.isfile(instance.image_path.path):
            os.remove(instance.image_path.path)
