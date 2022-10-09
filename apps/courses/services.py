from django.db.models import Prefetch, Q
from django.utils.timezone import localtime

from apps.courses.models import Course, CourseManagement, Lesson, CourseDocument
from apps.courses.enums import BOUGHT, PENDING
from apps.courses.exceptions import CheckElementExistException


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
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file"))),
            ),
            Prefetch("docs_completed"),
            Prefetch("videos_completed"),
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

    @staticmethod
    def add_doc_completed(course_mngt, doc):
        docs_completed = course_mngt.docs_completed.all()
        is_completed = False
        signal = False

        for lesson in course_mngt.course.lessons.all():
            if doc in lesson.documents.all():
                if doc not in docs_completed:
                    course_mngt.docs_completed.add(doc)
                    is_completed = True
                else:
                    course_mngt.docs_completed.remove(doc)
                signal = True
        if not signal:
            raise CheckElementExistException
        return is_completed

    @staticmethod
    def add_video_completed(course_mngt, video):
        videos_completed = course_mngt.videos_completed.all()
        is_completed = False
        signal = False

        for lesson in course_mngt.course.lessons.all():
            if video in lesson.videos.all():
                if video not in videos_completed:
                    course_mngt.videos_completed.add(video)
                    is_completed = True
                else:
                    course_mngt.videos_completed.remove(video)
                signal = True
        if not signal:
            raise CheckElementExistException("Video is not in course.")
        return is_completed


