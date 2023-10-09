from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.documents.models import Document
from apps.users.services import get_users_to_create_doc_mngt
from apps.core.general.init_data import InitDocumentServices


@receiver(post_save, sender=Document)
def init_document_rating(created, instance, **kwargs):
    if created:
        users = get_users_to_create_doc_mngt(instance)
        if users.count() > 0:
            InitDocumentServices().init_doc_mngt(instance, users)
