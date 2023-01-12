from typing import Any, Dict, List, Tuple
from apps.settings.models import HeaderDetail


def parse_choices(choices: List[Tuple]) -> List[Dict[str, Any]]:
    return [{"value": i[0], "label": i[1]} for i in choices]


def get_obj_type(header_detail: HeaderDetail):
    if header_detail.document_title:
        return "document"
    elif header_detail.course_title:
        return "course"
    else:
        return ""



# theem type get all docs, courses
# bỏ authen cho get all docs, courses
