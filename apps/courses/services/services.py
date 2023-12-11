from typing import List, Dict
from django.db.models import Prefetch, Q

from apps.courses.models import (
    Course,
    Lesson,
    CourseDocument,
    CourseManagement,
    CourseDocumentManagement,
    VideoManagement,
)
from apps.courses.enums import BOUGHT, PENDING, IN_PROGRESS, COMPLETED
from apps.core.utils import bulk_create_batch_size


class CourseService:
    @property
    def get_all_courses_queryset(self):
        return Course.objects.prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file")))
            )
        ).select_related('topic', 'thumbnail', 'author')

    def get_courses_by_topic(self, topic: str):
        if topic.strip():
            return self.get_all_courses_queryset.filter(
                course_of_class=False,
                topic__name__icontains=topic.strip(),
                is_selling=True,
            )
        return Course.objects.none()

    def get_courses_by_list_id(self, list_id: list):
        if list_id:
            return self.get_all_courses_queryset.filter(
                id__in=list_id, is_selling=True, course_of_class=False,
            )
        return Course.objects.none()

    @staticmethod
    def convert_structure(structure: List[Dict]):
        res = {}
        for obj in structure:
            if obj.get("lesson_id") and obj.get("quiz"):
                res[obj.get("lesson_id")] = obj.get("quiz")
        return res


class CourseManagementService:
    def __init__(self, user):
        self.user = user

    @property
    def get_all_course_management_queryset(self):
        return CourseManagement.objects.prefetch_related(
            Prefetch("course__lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file"))),
            ),
        ).select_related("user", "course__topic", "course__thumbnail").filter(user=self.user)

    @property
    def get_course_management_queryset(self):
        return self.get_all_course_management_queryset.filter(course__course_of_class=False)

    @property
    def get_course_mngt_queryset_by_selling(self):
        query = Q(course__is_selling=True)
        query |= Q(Q(course__is_selling=False) & Q(sale_status__in=[BOUGHT, PENDING]))
        return self.get_course_management_queryset.filter(query).order_by('course__name')

    def get_courses_mngt_by_list_id(self, list_id: list):
        if list_id:
            return self.get_course_mngt_queryset_by_selling.filter(course_id__in=list_id)

    def calculate_course_progress(self, course_id):
        progress = 0
        all_docs = CourseDocumentManagement.objects.filter(
            user=self.user, course_id=course_id, is_available=True, enable=True
        )
        all_videos = VideoManagement.objects.filter(
            user=self.user, course_id=course_id, is_available=True, enable=True
        )
        if all_videos.exists() or all_docs.exists():
            docs_completed = all_docs.filter(is_completed=True)
            videos_completed = all_videos.filter(is_completed=True)
            progress = round(
                100 * (docs_completed.count() + videos_completed.count()) / (all_docs.count() + all_videos.count())
            )

        if progress >= 100:
            CourseManagement.objects.filter(user=self.user, course_id=course_id).update(progress=progress, status=COMPLETED)
        elif progress < 100:
            CourseManagement.objects.filter(user=self.user, course_id=course_id).update(progress=progress, status=IN_PROGRESS)

        return progress

    def init_courses_management(self):
        if not CourseManagement.objects.filter(user=self.user).first():
            CourseManagement.objects.bulk_create([
                CourseManagement(user=self.user, course=course)
                for course in CourseService().get_all_courses_queryset.filter(course_of_class=False, is_selling=True)
            ])

    def update_lesson_progress(self, course_id: str, lessons: list):
        documents_id = []
        videos_id = []
        for lesson in lessons:
            documents_id.extend(lesson["completed_docs"])
            videos_id.extend(lesson["completed_videos"])

        # set False only this course, set True for all course
        CourseDocumentManagement.objects.filter(user=self.user, course_id=course_id, is_available=True).update(is_completed=False)
        CourseDocumentManagement.objects.filter(user=self.user, document_id__in=documents_id, is_available=True).update(is_completed=True)
        VideoManagement.objects.filter(user=self.user, course_id=course_id, is_available=True).update(is_completed=False)
        VideoManagement.objects.filter(user=self.user, video_id__in=videos_id, is_available=True).update(is_completed=True)

        return self.calculate_course_progress(course_id)

    def update_course_sale_status(self, courses, sale_status):
        CourseManagement.objects.filter(user=self.user, course__in=courses).update(sale_status=sale_status)

    def enable_courses_data(self, courses):
        CourseDocumentManagement.objects.filter(user=self.user, course__in=courses).update(is_available=True)
        VideoManagement.objects.filter(user=self.user, course__in=courses).update(is_available=True)

    def disable_courses_data(self, courses):
        CourseDocumentManagement.objects.filter(user=self.user, course__in=courses).update(is_available=False)
        VideoManagement.objects.filter(user=self.user, course__in=courses).update(is_available=False)

    def create_user_data_for_specific_course(self, instance: Course):
        lessons = instance.lessons.all()
        if not lessons:
            return

        course_doc_mngt = []
        video_mngt = []

        for lesson in lessons:
            course_docs = lesson.documents.only("id").values_list("pk", flat=True)
            if course_docs:
                existing_docs = CourseDocumentManagement.objects.filter(
                    course=instance, lesson=lesson, document_id__in=course_docs, user=self.user
                ).values_list("document_id", flat=True).distinct()
                docs_to_create = set(course_docs).difference(set(existing_docs))
                course_doc_mngt.extend([
                    CourseDocumentManagement(course=instance, lesson=lesson, document_id=doc_id, user=self.user)
                    for doc_id in docs_to_create
                ])

            videos = lesson.videos.only("id").values_list("pk", flat=True)
            if videos:
                existing_videos = VideoManagement.objects.filter(
                    course=instance, lesson=lesson, video_id__in=videos, user=self.user
                ).values_list("video_id", flat=True).distinct()
                videos_to_create = set(videos).difference(set(existing_videos))
                video_mngt.extend([
                    VideoManagement(course=instance, lesson=lesson, video_id=video_id, user=self.user)
                    for video_id in videos_to_create
                ])

        bulk_create_batch_size(CourseDocumentManagement, course_doc_mngt) if course_doc_mngt else []
        bulk_create_batch_size(VideoManagement, video_mngt) if video_mngt else []
