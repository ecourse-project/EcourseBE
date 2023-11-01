from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.documents.models import Document
from apps.core.general.init_data import init_doc_data_multiple_users
from apps.users.services import get_active_users


@receiver(post_save, sender=Document)
def create_user_data(created, instance, **kwargs):
    if created:
        users = get_active_users()
        init_doc_data_multiple_users(users)


