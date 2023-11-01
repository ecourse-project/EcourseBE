from apps.courses.enums import IN_PROGRESS, COMPLETED


def calculate_course_progress(course_mngt):
    total = course_mngt.total_docs_videos
    progress = round(100 * course_mngt.total_docs_videos_completed / total) if total != 0 else 0
    if progress >= 100:
        course_mngt.status = COMPLETED
    elif progress < 100:
        course_mngt.status = IN_PROGRESS
    course_mngt.progress = progress
    course_mngt.save(update_fields=['progress', 'status'])


def calculate_lesson_progress(lesson_mngt):
    total = lesson_mngt.total_docs_videos
    lesson_mngt.progress = round(100 * lesson_mngt.total_docs_videos_completed / total) if total != 0 else 0
    lesson_mngt.save(update_fields=['progress'])
