import os

from django.db.models.signals import post_delete
from django.dispatch import Signal, receiver

from apps.documents.models import Document
from django.conf import settings


@receiver(post_delete, sender=Document)
def delete_folder(sender, instance, **kwargs):
    directories = []
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for d in dirs:
            directories.append(os.path.join(root, d))

    for i in range(len(directories) - 1, -1, -1):
        if not os.listdir(directories[i]):
            os.rmdir(directories[i])
