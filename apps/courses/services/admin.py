from django.utils.timezone import localtime

from apps.courses.models import LessonManagement, CourseDocumentManagement, VideoManagement, CourseManagement
from apps.courses.enums import BOUGHT
from apps.users.models import User
from apps.courses.services.services import CourseManagementService


class CourseAdminService:
    def __init__(self, user):
        self.user = user

    def update_course_sale_status(self, courses, sale_status):
        CourseManagement.objects.filter(
            user=self.user, course__in=courses
        ).update(sale_status=sale_status, last_update=localtime())

    def init_courses_data(self, courses):
        for course in courses:
            all_lessons = course.lessons.all()
            for lesson in all_lessons:
                """ Initial documents of course """
                CourseDocumentManagement.objects.bulk_create([
                    CourseDocumentManagement(user=self.user, document=document, lesson=lesson, course=course)
                    for document in lesson.documents.all()
                ])
                """ Initial videos """
                VideoManagement.objects.bulk_create([
                    VideoManagement(user=self.user, video=video, lesson=lesson, course=course)
                    for video in lesson.videos.all()
                ])
            """ Initial lessons """
            for lesson in all_lessons:
                LessonManagement.objects.get_or_create(lesson=lesson, course=course)

    def disable_courses_data(self, courses):
        CourseDocumentManagement.objects.filter(user=self.user, course__in=courses).update(is_available=False)


def get_users_by_course_sale_status(course_id, sale_status):
    return CourseManagement.objects.filter(course_id=course_id, sale_status=sale_status).values_list("user_id", flat=True)


def init_course_mngt(course, users):
    CourseManagement.objects.bulk_create([CourseManagement(course=course, user=user) for user in users])


def insert_remove_docs_videos(course_id, lesson_id, docs_remove, videos_remove, docs_add, videos_add):
    courses_include_lesson = [course_id] if course_id else []
    if not courses_include_lesson:
        courses_include_lesson = (
            LessonManagement.objects.filter(lesson_id=lesson_id)
            .distinct("course_id")
            .values_list("course_id", flat=True)
        )

    for course_id in courses_include_lesson:
        user_ids = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
        if user_ids:
            is_update_mark = False
            if docs_remove:
                is_update_mark = True
                CourseDocumentManagement.objects.filter(
                    course_id=course_id, lesson_id=lesson_id, document__in=docs_remove, is_completed=False,
                ).delete()
                CourseDocumentManagement.objects.filter(
                    course_id=course_id, lesson_id=lesson_id, document__in=docs_remove, is_completed=True,
                ).update(is_available=False)
            if videos_remove:
                is_update_mark = True
                VideoManagement.objects.filter(
                    course_id=course_id, lesson_id=lesson_id, video__in=videos_remove, is_completed=False,
                ).delete()
                VideoManagement.objects.filter(
                    course_id=course_id, lesson_id=lesson_id, video__in=videos_remove, is_completed=True,
                ).update(is_available=False)
            if docs_add:
                is_update_mark = True
                for doc in docs_add:
                    for user_id in user_ids:
                        doc_obj, _ = CourseDocumentManagement.objects.get_or_create(
                            course_id=course_id, lesson_id=lesson_id, user_id=user_id, document=doc
                        )
                        if doc_obj:
                            doc_obj.is_available = True
                            doc_obj.save(update_fields=["is_available"])
            if videos_add:
                is_update_mark = True
                for video in videos_add:
                    for user_id in user_ids:
                        video_obj, _ = VideoManagement.objects.get_or_create(
                            course_id=course_id, lesson_id=lesson_id, user_id=user_id, video=video
                        )
                        if video_obj:
                            video_obj.is_available = True
                            video_obj.save(update_fields=["is_available"])

            if is_update_mark:
                for user_id in user_ids:
                    CourseManagementService(User.objects.get(id=user_id)).calculate_course_progress(course_id=course_id)
