from django.db import models
from django.dispatch import receiver

from apps.classes.models import Class
from apps.users.services import get_users_to_create_course_mngt
from apps.core.general.init_data import InitCourseServices


@receiver(models.signals.post_save, sender=Class)
def create_user_data(created, instance, **kwargs):
    if instance.course_of_class:
        users = get_users_to_create_course_mngt(instance)
        if users.exists():
            InitCourseServices().init_course_mngt(instance, users)

