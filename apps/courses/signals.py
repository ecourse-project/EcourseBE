from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.courses.models import CourseManagement, LessonManagement, Course
from apps.courses.enums import IN_PROGRESS, COMPLETED
from apps.rating.models import CourseRating
from apps.users.services import get_active_users
from apps.courses.services.admin import init_course_mngt


def calculate_course_progress(course_mngt):
    total = course_mngt.total_docs_videos
    progress = round(100 * course_mngt.total_docs_videos_completed / total) if total != 0 else 0
    if progress == 100:
        course_mngt.status = COMPLETED
    elif progress < 100:
        course_mngt.status = IN_PROGRESS
    course_mngt.progress = progress
    course_mngt.save(update_fields=['progress', 'status'])


def calculate_lesson_progress(lesson_mngt):
    total = lesson_mngt.total_docs_videos
    lesson_mngt.progress = round(100 * lesson_mngt.total_docs_videos_completed / total) if total != 0 else 0
    lesson_mngt.save(update_fields=['progress'])


@receiver(post_save, sender=Course)
def create_rating(created, instance, **kwargs):
    if created:
        CourseRating.objects.create(course=instance)
        users = get_active_users()
        if users.count() > 0:
            init_course_mngt(instance, users)

# @receiver(m2m_changed, sender=LessonManagement.docs_completed.through)
# def update_lesson_course_progress(sender, instance: LessonManagement, action, model, pk_set, **kwargs):
#     if action == "post_add" or action == "post_remove":
#         calculate_lesson_progress(instance)
#         course_mngt = CourseManagement.objects.filter(user=instance.user, course=instance.course).first()
#         calculate_course_progress(course_mngt)
#
#
# @receiver(m2m_changed, sender=LessonManagement.videos_completed.through)
# def update_lesson_course_progress(sender, instance: LessonManagement, action, model, pk_set, **kwargs):
#     if action == "post_add" or action == "post_remove":
#         calculate_lesson_progress(instance)
#         course_mngt = CourseManagement.objects.filter(user=instance.user, course=instance.course).first()
#         calculate_course_progress(course_mngt)
