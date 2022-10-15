from django.db.models import Prefetch, Q
from django.utils.timezone import localtime

from apps.courses.models import Course, CourseManagement, Lesson, CourseDocument
from apps.courses.enums import BOUGHT, PENDING
from apps.courses.exceptions import CheckElementExistException, NoItemException
from apps.upload.models import UploadFile



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
    def check_docs_videos_in_course(course_mngt, docs_set, videos_set):
        total = 0
        for lesson in course_mngt.course.lessons.all():
            same_docs = docs_set.intersection(set(lesson.documents.all()))
            same_videos = videos_set.intersection(set(lesson.videos.all()))
            total += len(same_docs) + len(same_videos)
        if total != len(docs_set) + len(videos_set):
            raise CheckElementExistException("Some documents or videos are not in course")

    def update_lesson_progress(self, course_id, docs_id, videos_id):
        course_mngt = CourseManagement.objects.filter(
            course_id=course_id, user=self.user, sale_status=BOUGHT).first()
        if not course_mngt:
            raise NoItemException

        docs = set(CourseDocument.objects.filter(id__in=docs_id))
        videos = set(UploadFile.objects.filter(id__in=videos_id))
        self.check_docs_videos_in_course(course_mngt, docs, videos)

        docs_completed = set(course_mngt.docs_completed.all())
        videos_completed = set(course_mngt.videos_completed.all())

        course_mngt.docs_completed.remove(*docs_completed.difference(docs))
        course_mngt.docs_completed.add(*docs.difference(docs_completed))
        course_mngt.videos_completed.remove(*videos_completed.difference(videos))
        course_mngt.videos_completed.add(*videos.difference(videos_completed))

        return dict(
            course_id=course_id,
            docs_completed=course_mngt.docs_completed.all().values_list('id', flat=True),
            videos_complated=course_mngt.videos_completed.all().values_list('id', flat=True),
        )

