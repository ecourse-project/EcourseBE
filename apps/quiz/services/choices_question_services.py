from typing import Dict

from apps.quiz.enums import(
    ANSWER_TYPE_TEXT,
    ANSWER_TYPE_IMAGE,
)


def transform_choices_text_to_dict(choices_text: str):
    choices_dict = {}
    try:
        if choices_text and isinstance(choices_text, str):
            choices_lst = choices_text.strip().split("\n")
            for choice in choices_lst:
                key_val = choice.split(":", 1)
                choices_dict[key_val[0].strip().upper()] = key_val[1].strip()
    except Exception:
        choices_dict = {}

    return choices_dict


def choices_quiz_data_processing(obj: Dict):
    obj_clone = obj.copy()

    # Custom content
    if obj_clone.get("content_type") == ANSWER_TYPE_TEXT:
        obj_clone["content"] = obj_clone.pop("content_text", "")
        obj_clone.pop("content_image", "")
    elif obj_clone.get("content_type") == ANSWER_TYPE_IMAGE:
        content_image = obj_clone.pop("content_image", "")
        obj_clone["content"] = content_image.get("image_path", "")
        obj_clone.pop("content_text", "")

    # Custom choices
    custom_choices = []
    choices = obj_clone.pop("choices", [])
    for choice in choices:
        choice_name = choice.get("choice_name")
        if choice_name and choice_name.get("id"):
            choice_dict = {
                "choice": choice_name.get("id"),
                "choice_name": choice_name.get("name"),
                "answer_type": choice["answer_type"],
                "answer": "",
            }
            if choice["answer_type"] == ANSWER_TYPE_TEXT:
                choice_dict["answer"] = choice["answer_text"]
            elif choice["answer_type"] == ANSWER_TYPE_IMAGE and isinstance(choice["answer_image"], dict):
                choice_dict["answer"] = choice["answer_image"].get("image_path", "")
            custom_choices.append(choice_dict)
    obj_clone["choices"] = custom_choices

    return obj_clone
