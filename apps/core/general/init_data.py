from typing import List, Tuple, Union

from django.db.models.query import QuerySet

from apps.core.utils import bulk_create_batch_size
from apps.users.models import User
from apps.users.choices import MANAGER
from apps.users.services import get_active_users

from apps.courses.models import *
from apps.documents.models import *
from apps.courses import enums as course_enums
from apps.documents import enums as doc_enums

from apps.documents.services.services import DocumentManagementService, DocumentService
from apps.courses.services.services import CourseManagementService, CourseService


class UserDataManagementService:
    def __init__(self, user: Union[User, None]):
        self.user = user
        self.doc_sv = DocumentService()
        self.doc_mngt_sv = DocumentManagementService(user)
        self.course_sv = CourseService()
        self.course_mngt_sv = CourseManagementService(user)

    def prepare_document_data(self) -> List[DocumentManagement]:
        all_docs = self.doc_sv.get_all_documents_queryset.values_list("pk", flat=True)
        existing_docs = self.doc_mngt_sv.get_doc_management_queryset.values_list("document_id", flat=True)
        doc_to_create = all_docs.difference(existing_docs)
        return [
            DocumentManagement(user=self.user, document_id=doc_id, sale_status=doc_enums.BOUGHT)
            if self.user.role == MANAGER
            else DocumentManagement(user=self.user, document_id=doc_id)
            for doc_id in doc_to_create
        ]

    @staticmethod
    def prepare_lesson_data_for_single_course(course, lessons: QuerySet) -> List[LessonManagement]:
        if lessons:
            lessons_id = lessons.values_list("pk", flat=True)
            existing_lesson_mngt = LessonManagement.objects.filter(
                course=course, lesson_id__in=lessons_id
            ).values_list("lesson_id", flat=True)
            lesson_to_create = lessons_id.difference(existing_lesson_mngt)
            return [LessonManagement(course=course, lesson_id=lesson_id) for lesson_id in lesson_to_create]
        return []

    def prepare_lesson_data_for_multiple_courses(self, courses) -> List[LessonManagement]:
        lesson_data = []
        for course in courses:
            lesson_data.extend(self.prepare_lesson_data_for_single_course(course, course.lessons.all()))
        return lesson_data

    @staticmethod
    def prepare_doc_video_data_for_single_course(course, lessons, user) -> (
            Tuple[List[CourseDocumentManagement], List[VideoManagement]]
    ):
        course_doc_to_create = []
        video_to_create = []

        if not lessons:
            return course_doc_to_create, video_to_create

        for lesson in lessons:
            doc_course = lesson.documents.all().values_list("pk", flat=True)
            user_course_doc_mngt = CourseDocumentManagement.objects.filter(
                course=course, lesson=lesson, user=user, document_id__in=doc_course
            ).values_list("document_id", flat=True)
            course_doc_to_create.extend([
                CourseDocumentManagement(course=course, lesson=lesson, user=user, document_id=doc_id)
                for doc_id in doc_course.difference(user_course_doc_mngt)
            ])

            video = lesson.videos.all().values_list("pk", flat=True)
            user_video_mngt = VideoManagement.objects.filter(
                course=course, lesson=lesson, user=user, video_id__in=video
            ).values_list("video_id", flat=True)
            video_to_create.extend([
                VideoManagement(course=course, lesson=lesson, user=user, video_id=video_id)
                for video_id in video.difference(user_video_mngt)
            ])

        return course_doc_to_create, video_to_create

    def prepare_doc_video_data_for_multiple_courses(self, courses, user) -> (
            Tuple[List[CourseDocumentManagement], List[VideoManagement]]
    ):
        course_doc_to_create = []
        video_to_create = []

        for course in courses:
            course_doc, video = self.prepare_doc_video_data_for_single_course(course, course.lessons.all(), user)
            course_doc_to_create.extend(course_doc)
            video_to_create.extend(video)

        return course_doc_to_create, video_to_create

    def prepare_course_data(self):
        courses = []
        lessons = []
        doc_courses = []
        videos = []

        all_courses = self.course_sv.get_all_courses_queryset.values_list("pk", flat=True)
        existing_courses = self.course_mngt_sv.get_all_course_management_queryset.values_list("course_id", flat=True)
        course_to_create = all_courses.difference(existing_courses)
        if course_to_create:
            course_objs = Course.objects.filter(pk__in=course_to_create)
            lessons = self.prepare_lesson_data_for_multiple_courses(course_objs)
            LessonManagement.objects.bulk_create(lessons) if lessons else []
            doc_courses, videos = self.prepare_doc_video_data_for_multiple_courses(course_objs, self.user)
            courses = [
                CourseManagement(
                    course_id=course_id,
                    user=self.user,
                    sale_status=course_enums.BOUGHT,
                    user_in_class=True,
                )
                if self.user.role == MANAGER
                else CourseManagement(course_id=course_id, user=self.user)
                for course_id in course_to_create
            ]

        return courses, lessons, doc_courses, videos

    @staticmethod
    def init_document_data(documents) -> List[DocumentManagement]:
        return bulk_create_batch_size(DocumentManagement, documents)

    # Include class
    @staticmethod
    def init_course_data(courses, doc_courses, videos):
        bulk_create_batch_size(CourseManagement, courses)
        bulk_create_batch_size(CourseDocumentManagement, doc_courses)
        bulk_create_batch_size(VideoManagement, videos)

    def init_user_course_data(self):
        courses, _, doc_courses, videos = self.prepare_course_data()
        self.init_course_data(courses, doc_courses, videos)

    def init_user_doc_data(self):
        documents = self.prepare_document_data()
        self.init_document_data(documents)

    def init_user_data(self):
        self.init_user_doc_data()
        self.init_user_course_data()

    @staticmethod
    def create_course_mngt_for_multiple_users(instance: Course, users=None):
        if not users:
            users = get_active_users()
        manager = users.filter(role=MANAGER)
        standard = users.difference(manager)

        course_mngt = [
            CourseManagement(course=instance, user=user)
            for user in standard
        ]
        course_mngt.extend([
            CourseManagement(course=instance, user=user, sale_status=course_enums.BOUGHT, user_in_class=True)
            for user in manager
        ])
        bulk_create_batch_size(CourseManagement, course_mngt) if course_mngt else []

        for user in manager:
            CourseManagementService(user).create_user_data_for_specific_course(instance)

    def create_multiple_course_mngt_for_user(self):
        all_courses = self.course_sv.get_all_courses_queryset.values_list("pk", flat=True)
        existing_courses = self.course_mngt_sv.get_all_course_management_queryset.values_list("course_id", flat=True)
        course_to_create = all_courses.difference(existing_courses)
        courses = [
            CourseManagement(course_id=course_id, user=self.user, sale_status=course_enums.BOUGHT, user_in_class=True)
            if self.user.role == MANAGER
            else CourseManagement(course_id=course_id, user=self.user)
            for course_id in course_to_create
        ]
        bulk_create_batch_size(CourseManagement, courses)

    def create_lesson_mngt(self, instance: Course, lessons: QuerySet):
        lesson_mngt = self.prepare_lesson_data_for_single_course(instance, lessons)
        bulk_create_batch_size(LessonManagement, lesson_mngt) if lesson_mngt else []


def init_all_data_multiple_users(users):
    for user in users:
        UserDataManagementService(user).init_user_data()


def init_doc_data_multiple_users(users):
    for user in users:
        UserDataManagementService(user).init_user_doc_data()


def init_course_data_multiple_users(users):
    courses = []
    doc_courses = []
    videos = []
    for user in users:
        c, _, d, v = UserDataManagementService(user).prepare_course_data()
        courses.extend(c)
        doc_courses.extend(d)
        videos.extend(v)

    if users:
        UserDataManagementService(None).init_course_data(courses, doc_courses, videos)


def init_doc_video_data_for_multiple_users(courses, users):
    sv = UserDataManagementService(None)
    doc_course_mngt = []
    video_mngt = []
    for user in users:
        doc_course, video = sv.prepare_doc_video_data_for_multiple_courses(courses, user)
        doc_course_mngt.extend(doc_course)
        video_mngt.extend(video)

    return (
        bulk_create_batch_size(CourseDocumentManagement, doc_course_mngt) if doc_course_mngt else [],
        bulk_create_batch_size(VideoManagement, video_mngt) if video_mngt else [],
    )
