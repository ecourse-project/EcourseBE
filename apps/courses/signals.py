from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.courses.models import Course
from apps.courses.enums import IN_PROGRESS, COMPLETED
from apps.users.services import get_users_to_create_course_mngt
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
def create_user_data(created, instance, **kwargs):
    # if created:
    #     # CourseRating.objects.create(course=instance)
    #     if not instance.course_of_class and users.exists() > 0:
    #         init_course_mngt(instance, users)

    if not instance.course_of_class:
        users = get_users_to_create_course_mngt(instance)
        if users.exists():
            init_course_mngt(instance, users)
