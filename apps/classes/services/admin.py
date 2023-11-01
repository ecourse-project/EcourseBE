from apps.classes.models import ClassManagement, ClassRequest


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


