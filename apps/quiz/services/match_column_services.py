from uuid import uuid4
from typing import List, Dict

from django.db.models import Q

from apps.quiz.enums import (
    ANSWER_TYPE_TEXT,
    ANSWER_TYPE_IMAGE,
)
from apps.quiz.models import (
    QuizManagement,
    MatchColumnMatchAnswer,
    MatchColumnUserAnswer,
    MatchColumnQuestion,
    MatchColumnContent,
)
from apps.quiz.enums import QUESTION_TYPE_MATCH


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


def init_match_question_column(column_data: List[Dict]) -> List[MatchColumnContent]:
    return [
        MatchColumnContent(
            pk=obj.get("id"),
            content_type=obj.get("content_type", ANSWER_TYPE_TEXT),
            content_text=obj.get("content"),
        )
        for obj in column_data
    ]


def match_question_processing(data: list):
    res = {}
    for question in data:
        pk = str(uuid4())
        instance = MatchColumnQuestion(pk=pk, content=question.get("content"))
        res[pk] = {
            "order": question.get("order", 1),
            "time_limit": question.get("time_limit", 10),
            "MatchColumnQuestion": instance,
            "first_column": init_match_question_column(question.get("first_column")),
            "second_column": init_match_question_column(question.get("second_column")),
            "correct_answer": question.get("correct_answer"),
        }
    return res


def store_match_question(data: list):
    res = match_question_processing(data)
    list_question = []
    list_content_instance = []
    list_question_mngt = []
    list_correct_answer = []
    for pk, info in res.items():
        list_question.append(info["MatchColumnQuestion"])
        list_content_instance.extend(info["first_column"])
        list_content_instance.extend(info["second_column"])
        list_correct_answer.extend(
            [
                MatchColumnMatchAnswer(
                    match_question_id=pk,
                    first_content_id=answers[0],
                    second_content_id=answers[1],
                )
                for answers in info["correct_answer"]
            ]
        )
        list_question_mngt.append(
            QuizManagement(
                order=info["order"],
                question_type=QUESTION_TYPE_MATCH,
                match_question=info["MatchColumnQuestion"],
                time_limit=info["time_limit"],
            )
        )

    if list_question:
        MatchColumnQuestion.objects.bulk_create(list_question)
    if list_content_instance:
        MatchColumnContent.objects.bulk_create(list_content_instance)
        for obj in list_question:
            obj.first_column.set(res[str(obj.pk)]["first_column"])
            obj.second_column.set(res[str(obj.pk)]["second_column"])
        if list_correct_answer:
            MatchColumnMatchAnswer.objects.bulk_create(list_correct_answer)

    return list_question_mngt


def delete_match_question(quiz_mngt: QuizManagement):
    if quiz_mngt and quiz_mngt.match_question:
        question = quiz_mngt.match_question
        first_column = question.first_column.all()
        second_column = question.second_column.all()
        [content.content_image.delete() for content in first_column if content.content_image]
        [content.content_image.delete() for content in second_column if content.content_image]
        first_column.delete()
        second_column.delete()
        question.delete()
        quiz_mngt.delete()


def get_total_correct_match(match_question: MatchColumnQuestion, first_column, second_column) -> List[List[str]]:
    res = []
    match_answers = MatchColumnMatchAnswer.objects.filter(
        # match_question=match_question,
        first_content__isnull=False,
        second_content__isnull=False,
    )
    match_answers_str = [[obj.first_content_id, obj.second_content_id] for obj in match_answers]

    for first_obj in first_column:
        for second_obj in second_column:
            if [first_obj.id, second_obj.id] in match_answers_str:
                res.append([str(first_obj.id), str(second_obj.id)])
            elif [second_obj.id, first_obj.id] in match_answers_str:
                res.append([str(second_obj.id), str(first_obj.id)])
    return res


def user_correct_quiz_match(user, course_id, lesson_id, created) -> List[Dict]:
    match_quiz = QuizManagement.objects.filter(
        Q(
            question_type=QUESTION_TYPE_MATCH,
            match_question__isnull=False,
            course_id=course_id,
            lesson_id=lesson_id,
        )
    )
    if not match_quiz:
        return []

    user_match_answers = MatchColumnUserAnswer.objects.filter(
        Q(
            created=created,
            user=user,
            quiz__in=match_quiz,
        )
    )

    res = []
    for quiz in match_quiz:
        quiz_info = {"quiz_id": str(quiz.id), "user_answer": [], "correct_answer": [], "correct": 0, "total": 0}
        correct_match = get_total_correct_match(
            quiz.match_question,
            quiz.match_question.first_column.all(),
            quiz.match_question.second_column.all(),
        )
        quiz_info["correct_answer"].extend(correct_match)
        quiz_info["total"] = len(correct_match)
        for answer in user_match_answers.filter(quiz_id=quiz.id):
            first = str(answer.first_content_id)
            second = str(answer.second_content_id)
            quiz_info["user_answer"].append([first, second])
            if [first, second] in correct_match or [second, first] in correct_match:
                quiz_info["correct"] += 1
        res.append(quiz_info)

    return res
