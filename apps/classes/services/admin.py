from apps.classes.models import ClassManagement, ClassRequest
from apps.core.general.init_data import InitCourseServices


def join_class_request(instance: ClassRequest):
    if instance.accepted:
        class_mngt, _ = ClassManagement.objects.get_or_create(user=instance.user, course=instance.class_request)
        class_mngt.user_in_class = True
        class_mngt.save(update_fields=["user_in_class"])
        InitCourseServices().init_course_data(instance.class_request, instance.user)

    elif not instance.accepted:
        class_mngt = ClassManagement.objects.filter(user=instance.user, course=instance.class_request, user_in_class=True).first()
        if class_mngt:
            class_mngt.user_in_class = False
            class_mngt.save(update_fields=["user_in_class"])
