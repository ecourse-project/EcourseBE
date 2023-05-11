from apps.courses.models import Course
from apps.classes.models import Class


def check_class_course(instance):
    return isinstance(instance, Course) or instance(instance, Class)