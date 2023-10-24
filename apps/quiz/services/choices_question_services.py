from uuid import uuid4
from typing import Dict

from django.db.models import Q

from apps.quiz.enums import (
    ANSWER_TYPE_TEXT,
    ANSWER_TYPE_IMAGE,
)
from apps.quiz.models import (
    QuizManagement,
    ChoicesQuizChoiceName,
    ChoicesQuizQuestion,
    ChoicesQuizAnswer,
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


def choices_question_processing(data):
    res = {}
    for question in data:
        pk = str(uuid4())
        correct_answer, _ = ChoicesQuizChoiceName.objects.get_or_create(name=question.get("correct_answer"))
        instance = ChoicesQuizQuestion(pk=pk, content_text=question.get("content"), correct_answer=correct_answer)
        res[pk] = {
            "order": question.get("order", 1),
            "time_limit": question.get("time_limit", 10),
            "ChoicesQuizQuestion": instance,
            "ChoicesQuizAnswer": []
        }
        for obj in question.get("choices", []):
            choice, _ = ChoicesQuizChoiceName.objects.get_or_create(name=obj.get("choice_name", ""))
            res[pk]["ChoicesQuizAnswer"].append(
                ChoicesQuizAnswer(
                    answer_text=obj.get("answer"),
                    answer_type=obj.get("answer_type", ANSWER_TYPE_TEXT),
                    choice_name=choice,
                )
            )
    return res


def store_choices_question(data):
    res = choices_question_processing(data)
    list_question = []
    list_answer_instance = []
    list_question_mngt = []
    for _, info in res.items():
        list_question.append(info["ChoicesQuizQuestion"])
        list_answer_instance.extend(info["ChoicesQuizAnswer"])
        list_question_mngt.append(
            QuizManagement(
                order=info["order"],
                question_type=QUESTION_TYPE_CHOICES,
                choices_question=info["ChoicesQuizQuestion"],
                time_limit=info["time_limit"],
            )
        )

    if list_answer_instance:
        ChoicesQuizAnswer.objects.bulk_create(list_answer_instance)
    if list_question:
        ChoicesQuizQuestion.objects.bulk_create(list_question)
        [obj.choices.set(res[str(obj.pk)]["ChoicesQuizAnswer"]) for obj in list_question]

    return list_question_mngt


def user_correct_quiz_choices(user, course_id, lesson_id, created) -> Dict:
    total_quiz = QuizManagement.objects.filter(
        Q(
            question_type=QUESTION_TYPE_CHOICES,
            choices_question__isnull=False,
            course_id=course_id,
            lesson_id=lesson_id,
        )
    )
    if not total_quiz:
        return {"result": [], "correct": 0, "total": 0}

    user_choice_answers = get_user_choice_answer_queryset().filter(
        Q(
            created=created,
            user=user,
            quiz__in=total_quiz,
        )
    )

    res = {"result": [], "correct": 0, "total": total_quiz.count()}
    if not user_choice_answers:
        return res

    for answer in user_choice_answers:
        choices_question = answer.quiz.choices_question
        res["result"].append(
            {
                "quiz_id": str(answer.quiz_id),
                "user_answer": str(answer.choice_id) if answer.choice else None,
                "correct_answer": str(choices_question.correct_answer_id) if choices_question.correct_answer else None,
            }
        )

    for result in res["result"]:
        if result["user_answer"] and result["correct_answer"] and result["user_answer"] == result["correct_answer"]:
            res["correct"] += 1

    return res
