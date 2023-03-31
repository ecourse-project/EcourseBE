from django.db.models import Prefetch

from apps.classes.models import Class, ClassRequest
from apps.classes.enums import ACCEPTED, REQUESTED, AVAILABLE
from apps.courses.models import Lesson, CourseDocument, Course
from apps.users.models import User


class ClassesService:
    @property
    def get_all_classes_queryset(self):
        return Class.objects.prefetch_related(
            Prefetch(
                "course__lessons",
                queryset=Lesson.objects.prefetch_related(
                    Prefetch("videos"),
                    Prefetch(
                        "documents",
                        queryset=CourseDocument.objects.select_related("file")
                    )))
        ).select_related("course", "topic")

    @property
    def get_course_of_class(self):
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
        if class_obj.users.filter(id=user.id).exists():
            return ACCEPTED
        elif ClassRequest.objects.filter(user=user, class_request=class_obj, accepted=False).exists():
            return REQUESTED
        else:
            return AVAILABLE
