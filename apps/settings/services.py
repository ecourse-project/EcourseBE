import datetime
from typing import Any, Dict, List, Tuple, Union

from apps.users.choices import MANAGER
from apps.core.general.enums import DOCUMENT, COURSE, CLASS, POST
from apps.settings.models import HeaderDetail, Header, HomePageDetail

from apps.courses.models import *


from apps.documents.models import *

from apps.classes.models import Class
from apps.posts.models import Post
from apps.core.utils import create_serializer_class


def parse_choices(choices: List[Tuple]) -> List[Dict[str, Any]]:
    return [{"value": i[0], "label": i[1]} for i in choices]


def get_header_query_type(header_detail: HeaderDetail):
    if header_detail.document_topic:
        return "document"
    elif header_detail.course_and_class_topic:
        return "course"
    # elif header_detail.class_topic:
    #     return "class"
    elif header_detail.post_topic:
        return "post"
    else:
        return ""


def get_first_n_object_by_created(documents, courses, classes, posts, n=9):
    data = []
    if isinstance(documents, list) and documents:
        document_serializer = create_serializer_class(Document, ("id", "created"))
        document_data = document_serializer(
            instance=Document.objects.filter(id__in=documents).only("id", "created"),
            many=True,
        ).data
        data.extend([{**doc, **{"type": DOCUMENT}} for doc in document_data])

    if isinstance(courses, list) and courses:
        course_serializer = create_serializer_class(Course, ("id", "created"))
        course_data = course_serializer(
            instance=Course.objects.filter(id__in=courses).only("id", "created"),
            many=True,
        ).data
        data.extend([{**course, **{"type": COURSE}} for course in course_data])

    if isinstance(classes, list) and classes:
        class_serializer = create_serializer_class(Class, ("id", "created"))
        class_data = class_serializer(
            instance=Class.objects.filter(id__in=classes).only("id", "created"),
            many=True,
        ).data
        data.extend([{**class_obj, **{"type": CLASS}} for class_obj in class_data])

    if isinstance(posts, list) and posts:
        post_serializer = create_serializer_class(Post, ("id", "created"))
        post_data = post_serializer(
            instance=Post.objects.filter(id__in=posts).only("id", "created"),
            many=True,
        ).data
        data.extend([{**post, **{"type": POST}} for post in post_data])

    sorted_data = sorted(
        data,
        key=lambda x: datetime.datetime.strptime(x['created'], '%Y-%m-%dT%H:%M:%S.%f'),
        reverse=True
    )

    return sorted_data[:n]


def get_home_page() -> list:
    homepage = []
    for obj in HomePageDetail.objects.all():
        sorted_data = get_first_n_object_by_created(
            documents=obj.documents,
            courses=obj.courses,
            classes=obj.classes,
            posts=obj.posts,
            n=obj.max_items_display,
        )
        homepage.append({
            "topic": obj.display_name,
            "detail": {
                'document_id': [obj["id"] for obj in sorted_data if obj["type"] == DOCUMENT] or None,
                'course_id': [obj["id"] for obj in sorted_data if obj["type"] == COURSE] or None,
                'class_id': [obj["id"] for obj in sorted_data if obj["type"] == CLASS] or None,
                'post_id': [obj["id"] for obj in sorted_data if obj["type"] == POST] or None,
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
            "topic": [
                {
                    "label": detail.display_name,
                    "value": getattr(
                        detail.document_topic or detail.course_and_class_topic or detail.post_topic, "name", ""
                    )
                } for detail in header_detail
            ] if header_detail.exists() else []
            # "type": get_header_query_type(header_detail.first()),
        })
    return list_header
