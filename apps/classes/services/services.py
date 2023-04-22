import uuid

from django.db.models import Prefetch, Q

from apps.classes.models import Class, ClassRequest, ClassManagement
from apps.classes.enums import ACCEPTED, REQUESTED, AVAILABLE
from apps.courses.models import Lesson, CourseDocument, Course
from apps.users.models import User


class ClassesService:
    @property
    def get_all_classes_queryset(self):
        return Course.objects.prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file")))
                     )
        ).select_related('topic', 'thumbnail').filter(course_of_class=True)

    def get_classes_by_topic(self, topic):
        if topic.strip():
            return self.get_all_classes_queryset.filter(topic__name__icontains=topic.strip())
        return Class.objects.none()

    def get_classes_by_list_id(self, list_id):
        if list_id:
            return self.get_all_classes_queryset.filter(id__in=list_id)
        return Class.objects.none()


class ClassRequestService:

    def get_user_request_status(self, user: User, class_obj: Class) -> str:
        if ClassRequest.objects.filter(user=user, class_request=class_obj, accepted=True).exists():
            return ACCEPTED
        elif ClassRequest.objects.filter(user=user, class_request=class_obj, accepted=False).exists():
            return REQUESTED
        else:
            return AVAILABLE

    def get_request_status_from_multiple_classes(self, user, class_objs):
        class_param = "class_request"
        if not isinstance(class_objs, Class) and not isinstance(class_objs, Course):
            class_param = "class_request__in"
            if class_objs and isinstance(class_objs[0], uuid.UUID) or isinstance(class_objs[0], str):
                class_param = "class_request_id__in"

        return ClassRequest.objects.filter(Q(**{class_param: class_objs}) & Q(user=user))

    def add_request_status(self, data, field, user, class_objs):
        request_objs_ids = self.get_request_status_from_multiple_classes(user, class_objs).values_list("class_request_id", flat=True)
        request_obj_accepted_ids = request_objs_ids.filter(accepted=True).values_list("class_request_id", flat=True)
        request_obj_requested_ids = request_objs_ids.difference(request_obj_accepted_ids)

        request_obj_accepted_ids = [str(obj_id) for obj_id in request_obj_accepted_ids]
        request_obj_requested_ids = [str(obj_id) for obj_id in request_obj_requested_ids]

        is_dict_data = isinstance(data, dict)
        if is_dict_data:
            data = [data]

        for index, obj in enumerate(data):
            if obj["id"] in request_obj_accepted_ids:
                data[index][field] = ACCEPTED
            elif obj["id"] in request_obj_requested_ids:
                data[index][field] = REQUESTED
            else:
                data[index][field] = AVAILABLE

        return data[0] if is_dict_data else data


class ClassManagementService:
    def __init__(self, user):
        self.user = user

    @property
    def get_class_management_queryset(self):
        return ClassManagement.objects.prefetch_related(
            Prefetch("course__lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file"))),
            ),
        ).select_related('course__topic', 'course__thumbnail').filter(user=self.user, course__course_of_class=True)

    # def add_request_status(self, data):
