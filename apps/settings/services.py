from typing import Any, Dict, List, Tuple

from apps.settings.models import HeaderDetail, Header, HomePageDetail
from apps.courses.services.services import CourseManagementService
from apps.documents.services.services import DocumentManagementService


def parse_choices(choices: List[Tuple]) -> List[Dict[str, Any]]:
    return [{"value": i[0], "label": i[1]} for i in choices]


def get_header_query_type(header_detail: HeaderDetail):
    if header_detail.document_topic:
        return "document"
    elif header_detail.course_topic:
        return "course"
    elif header_detail.class_topic:
        return "class"
    elif header_detail.post_topic:
        return "post"
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
                'class_id': obj.classes,
                'post_id': obj.posts,
            }
        })
    return homepage


def get_headers() -> list:
    list_header = []
    for header in Header.objects.all():
        header_detail = header.header_detail.all().order_by("display_name")
        list_header.append({
            "header": header.display_name,
            "type": header.data_type.lower() if header.data_type else "",
            "topic": [detail.display_name for detail in header_detail] if header_detail.exists() else []
            # "type": get_header_query_type(header_detail.first()),
        })
    return list_header


class UserDataManagementService:
    def __init__(self, user):
        self.user = user

    def init_user_data(self):
        DocumentManagementService(self.user).init_documents_management()
        CourseManagementService(self.user).init_courses_management()
