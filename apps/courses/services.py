from django.db.models import Prefetch, Q
from django.utils.timezone import localtime

from apps.courses.models import Course, CourseManagement, Lesson, CourseDocument
from apps.courses.enums import BOUGHT, PENDING


class CourseService:
    def __init__(self, user):
        self.user = user

    @property
    def get_all_courses_queryset(self):
        return Course.objects.prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file")))
                     )
        ).select_related('topic', 'thumbnail')


class CourseManagementService:
    def __init__(self, user):
        self.user = user

    @property
    def get_course_management_queryset(self):
        return CourseManagement.objects.prefetch_related(
            Prefetch("course__lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file")))
            )
        ).select_related('course__topic', 'course__thumbnail').filter(user=self.user)

    def init_courses_management(self):
        if not CourseManagement.objects.filter(user=self.user).first():
            CourseManagement.objects.bulk_create([
                CourseManagement(
                    user=self.user, course=course, last_update=localtime()
                ) for course in CourseService(self.user).get_all_courses_queryset
            ])

    @property
    def get_course_mngt_queryset_by_selling(self):
        query = Q(course__is_selling=True)
        query |= Q(course__is_selling=False) & Q(sale_status__in=[BOUGHT, PENDING])
        return self.get_course_management_queryset.filter(query)


