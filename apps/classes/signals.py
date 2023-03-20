from django.db import models
from django.dispatch import receiver

from apps.classes.models import Class, ClassRequest


@receiver(models.signals.post_save, sender=ClassRequest)
def add_and_remove_user_in_class(sender, instance, **kwargs):
    if instance.accepted:
        instance.class_request.users.add(instance.user)
    if not instance.accepted:
        instance.class_request.users.remove(instance.user)


