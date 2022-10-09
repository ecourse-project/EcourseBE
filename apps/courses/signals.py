from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.courses.models import CourseManagement


def calculate_progress(course_mngt):
    total = 0
    for lesson in course_mngt.course.lessons.all():
        total += lesson.total_docs_videos
    course_mngt.progress = round(100 * course_mngt.total_completed / total) if total != 0 else 0
    course_mngt.save(update_fields=['progress'])


@receiver(m2m_changed, sender=CourseManagement.docs_completed.through)
def update_cart_total_price_signal(sender, instance: CourseManagement, action, model, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove":
        calculate_progress(instance)


@receiver(m2m_changed, sender=CourseManagement.videos_completed.through)
def update_cart_total_price_signal(sender, instance: CourseManagement, action, model, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove":
        calculate_progress(instance)
