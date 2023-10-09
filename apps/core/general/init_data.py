from apps.users.models import User
from apps.users.choices import MANAGER

from apps.courses.models import (
    Course,
    CourseManagement,
    LessonManagement,
    CourseDocumentManagement,
    VideoManagement,
)
from apps.documents.models import (
    Document,
    DocumentManagement,
)
from apps.courses import enums as course_enums
from apps.documents import enums as doc_enums


class InitCourseServices:
    @staticmethod
    def init_lesson_data(course: Course):
        lessons = course.lessons.all()
        if lessons:
            user_lesson_mngt = LessonManagement.objects.filter(course=course, lesson__in=lessons)
            lesson_to_create_mngt = [
                LessonManagement(course=course, lesson_id=lesson_id)
                for lesson_id in
                lessons.values_list("id", flat=True).difference(user_lesson_mngt.values_list("lesson_id", flat=True))
            ]
            LessonManagement.objects.bulk_create(lesson_to_create_mngt) if lesson_to_create_mngt else None

        return lessons

    @staticmethod
    def init_doc_video_data(course: Course, lessons, user: User):
        if lessons:
            course_doc_to_create_mngt = []
            video_to_create_mngt = []
            for lesson in lessons:
                doc_course = lesson.documents.all()
                user_course_doc_mngt = CourseDocumentManagement.objects.filter(
                    course=course, lesson=lesson, user=user, document__in=doc_course
                )
                course_doc_to_create_mngt.extend(
                    [
                        CourseDocumentManagement(course=course, lesson=lesson, user=user, document_id=doc_id) for doc_id in
                        doc_course.values_list("id", flat=True).difference(user_course_doc_mngt.values_list("document_id", flat=True))
                    ]
                )

                video = lesson.videos.all()
                user_video_mngt = VideoManagement.objects.filter(course=course, lesson=lesson, user=user, video__in=video)
                video_to_create_mngt.extend(
                    [
                        VideoManagement(course=course, lesson=lesson, user=user, video_id=vid_id) for vid_id in
                        video.values_list("id", flat=True).difference(user_video_mngt.values_list("video_id", flat=True))
                    ]
                )

            CourseDocumentManagement.objects.bulk_create(course_doc_to_create_mngt) if course_doc_to_create_mngt else None
            VideoManagement.objects.bulk_create(video_to_create_mngt) if video_to_create_mngt else None

    def init_course_data(self, course: Course, user: User):
        if course and user:
            lesson = self.init_lesson_data(course)
            self.init_doc_video_data(course, lesson, user)

    @staticmethod
    def prepare_course_mngt_to_create(course: Course, users):
        return [
            CourseManagement(course=course, user=user, sale_status=course_enums.BOUGHT, user_in_class=True)
            if user.role == MANAGER
            else CourseManagement(course=course, user=user)
            for user in users
        ]

    def init_course_mngt(self, course, users):
        return CourseManagement.objects.bulk_create(self.prepare_course_mngt_to_create(course, users))


class InitDocumentServices:
    @staticmethod
    def prepare_doc_to_create(document: Document, users):
        return [
            DocumentManagement(document=document, user=user, sale_status=doc_enums.BOUGHT)
            if user.role == MANAGER
            else DocumentManagement(document=document, user=user)
            for user in users
        ]

    def init_doc_mngt(self, document: Document, users):
        return DocumentManagement.objects.bulk_create(self.prepare_doc_to_create(document, users))
