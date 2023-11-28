from django.db.models import Q
from django.db.models.query import QuerySet

from apps.courses.models import (
    LessonManagement,
    CourseDocumentManagement,
    VideoManagement,
    Course,
    Lesson,
)

from apps.core.general.init_data import (
    UserDataManagementService,
    init_doc_video_data_for_multiple_users,
)
from apps.core.utils import bulk_create_batch_size
from apps.users.services import get_active_users
from apps.users.choices import MANAGER


class AdminCoursePermissons:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def course_condition():
        return Q(course_of_class=False)

    @staticmethod
    def course_condition_fk(fk_field):
        return Q(**{f"{fk_field}__course_of_class": False})

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
            self.course_condition() & self.user_condition()
            if not fk_field
            else self.course_condition_fk(fk_field) & self.user_condition_fk(fk_field)
        )


class CourseAdminService:
    @staticmethod
    def add_course_data_admin(instance, lessons_add):
        if isinstance(lessons_add, QuerySet):
            lessons_qs = lessons_add
        else:
            lessons_qs = Lesson.objects.filter(pk__in=[lesson.pk for lesson in lessons_add])

        sv = UserDataManagementService(None)
        users = get_active_users()
        lesson_mngt = sv.prepare_lesson_data_for_single_course(instance, lessons_qs)
        bulk_create_batch_size(LessonManagement, lesson_mngt) if lesson_mngt else []
        course_doc, video = init_doc_video_data_for_multiple_users([instance], users)
        if not course_doc:
            CourseDocumentManagement.objects.filter(course=instance, lesson__in=lessons_add).update(is_available=True)
        if not video:
            VideoManagement.objects.filter(course=instance, lesson__in=lessons_add).update(is_available=True)

    def add_lesson_data_admin(self, instance: Lesson, docs_add_id, videos_add_id):
        courses = instance.courses.all()
        for course in courses:
            self.create_doc_video_mngt(
                instance=course,
                lesson=instance,
                docs_add_id=docs_add_id,
                videos_add_id=videos_add_id,
            )

    @staticmethod
    def create_doc_video_mngt(instance: Course, lesson: Lesson, users=None, docs_add_id=None, videos_add_id=None):
        if not users:
            users = get_active_users()
        users_id = users.values_list("id", flat=True)

        course_doc_mngt = []
        video_mngt = []

        # CourseDocumentManagement
        course_docs = lesson.documents.only("id")
        for doc in course_docs:
            existing_user_docs = CourseDocumentManagement.objects.filter(
                course=instance, lesson=lesson, document=doc, user__in=users
            ).values_list("user_id", flat=True).distinct()
            users_to_create = set(users_id).difference(set(existing_user_docs))
            course_doc_mngt.extend([
                CourseDocumentManagement(course=instance, lesson=lesson, document=doc, user_id=user_id)
                for user_id in users_to_create
            ])

        # VideoManagement
        videos = lesson.videos.only("id")
        for video in videos:
            existing_user_videos = VideoManagement.objects.filter(
                course=instance, lesson=lesson, video=video, user__in=users
            ).values_list("user_id", flat=True).distinct()
            users_to_create = set(users_id).difference(set(existing_user_videos))
            video_mngt.extend([
                VideoManagement(course=instance, lesson=lesson, video=video, user_id=user_id)
                for user_id in users_to_create
            ])

        if docs_add_id is None and videos_add_id is None:
            CourseDocumentManagement.objects.filter(course=instance, lesson=lesson).update(is_available=True)
            VideoManagement.objects.filter(course=instance, lesson=lesson).update(is_available=True)
        elif docs_add_id is not None and videos_add_id is not None:
            if docs_add_id:
                CourseDocumentManagement.objects.filter(
                    course=instance, lesson=lesson, document_id__in=docs_add_id
                ).update(is_available=True)
            if videos_add_id:
                VideoManagement.objects.filter(
                    course=instance, lesson=lesson, video_id__in=videos_add_id
                ).update(is_available=True)

        return (
            bulk_create_batch_size(CourseDocumentManagement, course_doc_mngt) if course_doc_mngt else [],
            bulk_create_batch_size(VideoManagement, video_mngt) if video_mngt else []
        )





