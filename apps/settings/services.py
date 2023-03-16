from typing import Any, Dict, List, Tuple
from django.utils.timezone import localtime

from apps.settings.models import HeaderDetail, Header, HomePageDetail
from apps.courses.models import CourseManagement
from apps.courses.services.services import CourseService
from apps.documents.services.services import DocumentManagementService


def parse_choices(choices: List[Tuple]) -> List[Dict[str, Any]]:
    return [{"value": i[0], "label": i[1]} for i in choices]


def get_header_query_type(header_detail: HeaderDetail):
    if header_detail.document_topic:
        return "document"
    elif header_detail.course_topic:
        return "course"
    else:
        return ""


def get_home_page() -> list:
    homepage = []
    for obj in HomePageDetail.objects.all():
        homepage.append({
            "topic": obj.display_name,
            "detail": {
                'document_id': obj.documents,
                'course_id': obj.courses,
            }
        })
    return homepage


def get_headers() -> list:
    list_header = []
    for header in Header.objects.all():
        header_detail = header.header_detail.all().order_by("display_name")
        list_header.append({
            "header": header.display_name,
            "detail": {
                "type": get_header_query_type(header_detail.first()),
                "topic": [detail.display_name for detail in header_detail]
            } if header_detail.exists() else {}
        })
    return list_header


class UserDataManagementService:
    def __init__(self, user):
        self.user = user

    def init_user_data(self):
        if not CourseManagement.objects.filter(user=self.user).first():
            CourseManagement.objects.bulk_create([
                CourseManagement(user=self.user, course=course, last_update=localtime())
                for course in CourseService().get_all_courses_queryset
            ])
        DocumentManagementService(self.user).init_documents_management()
