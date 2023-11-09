from django.db.models import Q

from apps.classes.models import ClassManagement, ClassRequest
from apps.users.choices import MANAGER


def join_class_single_request(instance: ClassRequest):
    class_mngt = ClassManagement.objects.get(user=instance.user, course=instance.class_request)
    class_mngt.user_in_class = instance.accepted
    class_mngt.save(update_fields=["user_in_class"])


def join_class_multiple_requests(instances, accepted: bool):
    classes_request = set([instance.class_request for instance in instances])
    classify_by_class = {
        class_obj: [instance.user for instance in instances if instance.class_request == class_obj]
        for class_obj in classes_request
    }
    for class_obj, users in classify_by_class.items():
        ClassManagement.objects.filter(course=class_obj, user__in=users).update(user_in_class=accepted)


class AdminClassPermissons:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def class_condition():
        return Q(course_of_class=True)

    @staticmethod
    def class_condition_fk(fk_field):
        return Q(**{f"{fk_field}__course_of_class": True})

    def user_condition(self):
        return (
            Q(author=self.user)
            if not self.user.is_superuser and not self.user.role == MANAGER
            else Q()
        )

    def user_condition_fk(self, fk_field):
        return (
            Q(**{f"{fk_field}__author": self.user})
            if not self.user.is_superuser and not self.user.role == MANAGER
            else Q()
        )

    def get_filter_condition(self, fk_field=None):
        return (
            self.class_condition() & self.user_condition()
            if not fk_field
            else self.class_condition_fk(fk_field) and self.user_condition_fk(fk_field)
        )
