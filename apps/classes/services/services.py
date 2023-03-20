from django.db.models import Prefetch

from apps.classes.models import Class
from apps.courses.models import Lesson, CourseDocument


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
        ).select_related("course")
