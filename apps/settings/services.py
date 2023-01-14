from typing import Any, Dict, List, Tuple
from apps.settings.models import HeaderDetail, Header, HomePageDetail


def parse_choices(choices: List[Tuple]) -> List[Dict[str, Any]]:
    return [{"value": i[0], "label": i[1]} for i in choices]


def get_header_query_type(header_detail: HeaderDetail):
    if header_detail.document_title:
        return "document"
    elif header_detail.course_title:
        return "course"
    else:
        return ""


def get_home_page() -> list:
    homepage = []
    for obj in HomePageDetail.objects.all():
        homepage.append({
            "title": obj.display_name,
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
                "title": [detail.display_name for detail in header_detail]
            } if header_detail.exists() else {}
        })
    return list_header


# theem type get all docs, courses
# bỏ authen cho get all docs, courses
