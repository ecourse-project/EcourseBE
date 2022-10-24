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
            LessonManagement.objects.bulk_create([
                LessonManagement(user=self.user, lesson=lesson, course=course) for lesson in all_lessons
            ])

    def disable_courses_data(self, courses):
        CourseDocumentManagement.objects.filter(user=self.user, course__in=courses).update(is_available=False)


def get_users_by_course_sale_status(course_id, sale_status):
    return CourseManagement.objects.filter(course_id=course_id, sale_status=sale_status).values_list("user_id", flat=True)


def init_course_mngt(course, users):
    CourseManagement.objects.bulk_create([CourseManagement(course=course, user=user) for user in users])


def add_docs_to_lesson(docs, lesson, courses_include_lesson):
    list_doc_objs = []
    for course_id in courses_include_lesson:
        users = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
        for user_id in users:

            for doc in docs:
                doc_obj, _ = CourseDocumentManagement.objects.get_or_create(
                    course_id=course_id, lesson=lesson, document=doc, user_id=user_id)
                if doc_obj:
                    doc_obj.is_available = True
                    list_doc_objs.append(doc_obj)
    CourseDocumentManagement.objects.bulk_update(list_doc_objs, ["is_available"])

    for course_id in courses_include_lesson:
        users = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
        for user_id in users:
            CourseManagementService(User.objects.get(id=user_id)).calculate_course_progress(course_id=course_id)


def add_videos_to_lesson(videos, lesson, courses_include_lesson):
    list_video_objs = []
    for course_id in courses_include_lesson:
        users = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
        for user_id in users:
            for video in videos:
                video_obj, _ = VideoManagement.objects.get_or_create(
                    course_id=course_id, lesson=lesson, video=video, user_id=user_id)
                if video_obj:
                    video_obj.is_available = True
                    list_video_objs.append(video_obj)
    VideoManagement.objects.bulk_update(list_video_objs, ["is_available"])

    for course_id in courses_include_lesson:
        users = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
        for user_id in users:
            CourseManagementService(User.objects.get(id=user_id)).calculate_course_progress(course_id=course_id)


def update_course_doc_mngt(docs_remove, docs_add, lesson, courses_include_lesson):
    if docs_remove:
        CourseDocumentManagement.objects.filter(document__in=docs_remove, lesson=lesson).update(is_available=False)
        for course_id in courses_include_lesson:
            users = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
            for user_id in users:
                CourseManagementService(User.objects.get(id=user_id)).calculate_course_progress(course_id=course_id)
    if docs_add:
        add_docs_to_lesson(docs=docs_add, lesson=lesson, courses_include_lesson=courses_include_lesson)


def update_video_mngt(videos_remove, videos_add, lesson, courses_include_lesson):
    if videos_remove:
        VideoManagement.objects.filter(video__in=videos_remove, lesson=lesson).update(is_available=False)
        for course_id in courses_include_lesson:
            users = get_users_by_course_sale_status(course_id=course_id, sale_status=BOUGHT)
            for user_id in users:
                CourseManagementService(User.objects.get(id=user_id)).calculate_course_progress(course_id=course_id)
    if videos_add:
        add_videos_to_lesson(videos=videos_add, lesson=lesson, courses_include_lesson=courses_include_lesson)
