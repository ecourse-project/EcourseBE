from typing import Dict

from apps.quiz.enums import (
    ANSWER_TYPE_TEXT,
    ANSWER_TYPE_IMAGE,
)


def match_column_quiz_data_processing(obj: Dict):
    obj_clone = obj.copy()

    if obj_clone.get("content_type") == ANSWER_TYPE_TEXT:
        obj_clone["content"] = obj_clone.pop("content_text", "")
        obj_clone.pop("content_image", "")
    elif obj_clone.get("content_type") == ANSWER_TYPE_IMAGE:
        content_image = obj_clone.pop("content_image", "")
        obj_clone["content"] = content_image.get("image_path", "")
        obj_clone.pop("content_text", "")

    return obj_clone