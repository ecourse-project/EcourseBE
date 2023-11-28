from uuid import uuid4
from typing import Dict

from django.db.models import Q

from apps.quiz.enums import (
    ANSWER_TYPE_TEXT,
    ANSWER_TYPE_IMAGE,
)
from apps.quiz.models import (
    Quiz,
    QuestionManagement,
    ChoiceName,
    ChoicesQuestion,
    ChoicesAnswer,
)
from apps.quiz.services.queryset_services import get_user_choice_answer_queryset
from apps.quiz.enums import QUESTION_TYPE_CHOICES


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


def choices_question_data_processing(obj: Dict):
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


def choices_question_processing(data: list, user):
    res = {}
    for question in data:
        pk = str(uuid4())
        correct_answer, _ = ChoiceName.objects.get_or_create(name=question.get("correct_answer"))
        instance = ChoicesQuestion(pk=pk, content_text=question.get("content"), correct_answer=correct_answer, author=user)
        res[pk] = {
            "order": question.get("order", 1),
            "time_limit": question.get("time_limit", 10),
            "ChoicesQuestion": instance,
            "ChoicesAnswer": []
        }
        for obj in question.get("choices", []):
            choice, _ = ChoiceName.objects.get_or_create(name=obj.get("choice_name", ""))
            res[pk]["ChoicesAnswer"].append(
                ChoicesAnswer(
                    answer_text=obj.get("answer"),
                    answer_type=obj.get("answer_type", ANSWER_TYPE_TEXT),
                    choice_name=choice,
                    author=user,
                )
            )
    return res


def store_choices_question(data: list, user):
    res = choices_question_processing(data, user)
    list_question = []
    list_answer_instance = []
    list_question_mngt = []
    for _, info in res.items():
        list_question.append(info["ChoicesQuestion"])
        list_answer_instance.extend(info["ChoicesAnswer"])
        list_question_mngt.append(
            QuestionManagement(
                order=info["order"],
                question_type=QUESTION_TYPE_CHOICES,
                choices_question=info["ChoicesQuestion"],
                time_limit=info["time_limit"],
            )
        )

    if list_answer_instance:
        ChoicesAnswer.objects.bulk_create(list_answer_instance)
    if list_question:
        ChoicesQuestion.objects.bulk_create(list_question)
        [obj.choices.set(res[str(obj.pk)]["ChoicesAnswer"]) for obj in list_question]

    return list_question_mngt


def delete_choices_question(question_mngt: QuestionManagement):
    if question_mngt and question_mngt.choices_question:
        question = question_mngt.choices_question
        choices = question.choices.all()
        for choice in choices:
            choice.answer_image.delete() if choice.answer_image else ""
        choices.delete()
        question.delete()
        question_mngt.delete()


def user_correct_question_choices(quiz: Quiz, user, created) -> Dict:
    choice_question = quiz.question_mngt.filter(
        Q(
            question_type=QUESTION_TYPE_CHOICES,
            choices_question__isnull=False,
        )
    )
    if not choice_question:
        return {"result": [], "correct": 0, "total": 0}

    user_choice_answers = get_user_choice_answer_queryset().filter(
        Q(
            created=created,
            user=user,
            question__in=choice_question,
        )
    )
    user_choice_answers_dict = {str(answer.question_id): str(answer.choice_id) for answer in user_choice_answers}

    res = {"result": [], "correct": 0, "total": choice_question.count()}
    for question_mngt in choice_question:
        question = question_mngt.choices_question
        question_mngt_id = str(question_mngt.id)
        res["result"].append(
            {
                "question_id": question_mngt_id,
                "user_answer": user_choice_answers_dict.get(question_mngt_id),
                "correct_answer": str(question.correct_answer_id) if question.correct_answer else None,
            }
        )
    # if not user_choice_answers:
    #     return res

    # for answer in user_choice_answers:
    #     choices_question = answer.question.choices_question
    #     res["result"].append(
    #         {
    #             "question_id": str(answer.question_id),
    #             "user_answer": str(answer.choice_id) if answer.choice else None,
    #             "correct_answer": str(choices_question.correct_answer_id) if choices_question.correct_answer else None,
    #         }
    #     )

    for result in res["result"]:
        if result["user_answer"] and result["correct_answer"] and result["user_answer"] == result["correct_answer"]:
            res["correct"] += 1

    return res
