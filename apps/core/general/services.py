
from apps.courses.models import LessonManagement, VideoManagement, CourseDocumentManagement
from apps.classes.services.services import ClassRequestService
from apps.core.general import enums


class CustomDataServices:
    def __init__(self, user=None):
        self.user = user
        self.class_request_service = ClassRequestService()

    def add_docs_videos_completed(self, data, doc_field, video_field):
        for index, lesson in enumerate(data['lessons'], start=0):
            lesson_mngt = LessonManagement.objects.filter(lesson_id=lesson['id']).first()
            if lesson_mngt:
                lesson_obj = lesson_mngt.lesson
                data["lessons"][index][doc_field] = CourseDocumentManagement.objects.filter(
                    user=self.user,
                    course_id=data['id'],
                    document__in=lesson_obj.documents.all(),
                    is_completed=True,
                    is_available=True,
                ).values_list('document', flat=True)
                data["lessons"][index][video_field] = VideoManagement.objects.filter(
                    user=self.user,
                    course_id=data['id'],
                    video__in=lesson_obj.videos.all(),
                    is_completed=True,
                    is_available=True,
                ).values_list('video', flat=True)
            else:
                data['lessons'][index]['docs_completed'] = []
                data['lessons'][index]['videos_completed'] = []

        return data

    def custom_response_data(self, data, **kwargs):
        fields = kwargs.get("fields", [])
        if enums.DOCS_COMPLETED in fields and enums.VIDEOS_COMPLETED in fields:
            data = self.add_docs_videos_completed(data, enums.DOCS_COMPLETED, enums.VIDEOS_COMPLETED)
            fields.remove(enums.DOCS_COMPLETED)
            fields.remove(enums.VIDEOS_COMPLETED)
        for field in fields:
            if field == enums.REQUEST_STATUS and kwargs.get("user") and kwargs.get("class_objs"):
                data = self.class_request_service.add_request_status(data, field, kwargs.get("user"), kwargs.get("class_objs"))
        return data