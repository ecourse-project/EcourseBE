# from celery import shared_task
#
# from apps.courses.models import Course, Lesson
# from apps.courses.services.admin import CourseAdminService
# from apps.core.general.init_data import UserDataManagementService
#
#
# @shared_task
# def init_course_data_multiple_users_task(course_id):
#     try:
#         course = Course.objects.get(pk=course_id)
#     except Course.DoesNotExist:
#         return
#
#     UserDataManagementService(None).create_course_mngt_for_multiple_users(course)
#
#
# # Lesson in course/class change
# @shared_task
# def course_lesson_change_admin_task(course_id, lessons_add_id):
#     try:
#         course = Course.objects.get(pk=course_id)
#         lessons_add = Lesson.objects.filter(pk__in=lessons_add_id)
#     except Course.DoesNotExist:
#         return
#
#     sv = CourseAdminService()
#     for lesson in lessons_add:
#         sv.create_doc_video_mngt(course, lesson)
#
#
# @shared_task()
# def add_lesson_data_admin_task(lesson_id, docs_add_id, videos_add_id):
#     try:
#         lesson = Lesson.objects.get(pk=lesson_id)
#     except Lesson.DoesNotExist:
#         return
#
#     CourseAdminService().add_lesson_data_admin(lesson, docs_add_id, videos_add_id)
#
#
#
#
