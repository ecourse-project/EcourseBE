from django.db import models
from django.dispatch import receiver

from apps.classes.models import ClassRequest
from apps.courses.models import CourseManagement
from apps.courses.services.admin import CourseAdminService


@receiver(models.signals.post_save, sender=ClassRequest)
def add_and_remove_user_in_class(sender, instance, **kwargs):
    if instance.accepted:
        instance.class_request.users.add(instance.user)
        course = instance.class_request.course
        if course:
            CourseManagement.objects.create(user=instance.user, course=course)
            course_service = CourseAdminService(instance.user)
            course_service.init_courses_data([course])

    if not instance.accepted:
        instance.class_request.users.remove(instance.user)


