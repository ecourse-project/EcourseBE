from django.db import models
from django.dispatch import receiver

from apps.classes.models import ClassRequest, ClassManagement, Class
from apps.courses.services.admin import CourseAdminService
from apps.users.services import get_users_to_create_course_mngt
from apps.courses.services.admin import init_course_mngt


@receiver(models.signals.post_save, sender=ClassRequest)
def add_and_remove_user_in_class(sender, instance, **kwargs):
    if instance.accepted:
        class_mngt = ClassManagement.objects.filter(user=instance.user, course=instance.class_request).first()
        if class_mngt:
            class_mngt.user_in_class = True
            class_mngt.save(update_fields=["user_in_class"])
        else:
            ClassManagement.objects.create(user=instance.user, course=instance.class_request, user_in_class=True)
            course_service = CourseAdminService(instance.user)
            course_service.init_courses_data([instance.class_request])

    if not instance.accepted:
        class_mngt = ClassManagement.objects.filter(user=instance.user, course=instance.class_request, user_in_class=True).first()
        if class_mngt:
            class_mngt.user_in_class = False
            class_mngt.save(update_fields=["user_in_class"])


@receiver(models.signals.post_save, sender=Class)
def create_user_data(created, instance, **kwargs):
    if instance.course_of_class:
        users = get_users_to_create_course_mngt(instance)
        if users.exists():
            init_course_mngt(instance, users)

