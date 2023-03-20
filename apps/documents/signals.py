import os

from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver
from django.conf import settings

from apps.documents.models import Document
from apps.rating.models import DocumentRating
from apps.users.services import get_active_users
from apps.documents.services.admin import init_doc_mngt


# @receiver(post_delete, sender=Document)
# def delete_folder(sender, instance, **kwargs):
#     directories = []
#     for root, dirs, files in os.walk(settings.MEDIA_ROOT):
#         for d in dirs:
#             directories.append(os.path.join(root, d))
#
#     for i in range(len(directories) - 1, -1, -1):
#         if not os.listdir(directories[i]):
#             os.rmdir(directories[i])


@receiver(post_save, sender=Document)
def init_document_rating(created, instance, **kwargs):
    if created:
        DocumentRating.objects.create(document=instance)
        users = get_active_users()
        if users.count() > 0:
            init_doc_mngt(instance, users)
