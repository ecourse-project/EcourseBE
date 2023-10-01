from typing import Dict, List

from django.db.models import Q, Prefetch

from apps.quiz.enums import (
    QUESTION_TYPE_CHOICES,
    QUESTION_TYPE_MATCH,
)
from apps.quiz.models import (
    ChoicesQuizUserAnswer,
    MatchColumnUserAnswer,
    QuizManagement,
    MatchColumnMatchAnswer,
    MatchColumnContent,
    ChoicesQuizAnswer,
)
from apps.configuration.models import Configuration


def get_quiz_queryset():
    return QuizManagement.objects.select_related(
            "course",
            "choices_question",
            "match_question",
        ).prefetch_related(
            Prefetch(
                "match_question__first_column",
                queryset=MatchColumnContent.objects.select_related("content_image")
            ),
            Prefetch(
                "match_question__second_column",
                queryset=MatchColumnContent.objects.select_related("content_image")
            ),
            Prefetch(
                "choices_question__choices",
                queryset=ChoicesQuizAnswer.objects.select_related("answer_image", "choice_name")
            ),
        )


def get_user_choice_answer_queryset(qs=None):
    res = qs if qs else ChoicesQuizUserAnswer.objects.all()
    return res.select_related(
            "user", "quiz", "choice",
        ).prefetch_related(
            Prefetch("quiz", queryset=get_quiz_queryset())
        )


def store_user_answers(user, user_answers):
    choice_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_CHOICES]
    match_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_MATCH]

    choice_answer_objs = [
        ChoicesQuizUserAnswer(
            user=user,
            quiz_id=choice_obj.get("quiz_id"),
            choice_id=choice_obj.get("answer")
        )
        for choice_obj in choice_type_objs
    ]

    match_answer_obj = [
        MatchColumnUserAnswer(
            user=user,
            quiz_id=match_obj.get("quiz_id"),
            first_content_id=answer[0],
            second_content_id=answer[1]
        )
        for match_obj in match_type_objs
        for answer in match_obj.get("answer")
    ]

    if choice_answer_objs:
        ChoicesQuizUserAnswer.objects.bulk_create(choice_answer_objs)
    if match_answer_obj:
        MatchColumnUserAnswer.objects.bulk_create(match_answer_obj)

    return choice_answer_objs, match_answer_obj


def user_correct_quiz_choices(user, course_id, lesson_id) -> Dict:
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
            user=user,
            quiz__in=total_quiz,
        )
    )

    res = {"result": [], "correct": 0, "total": total_quiz.count()}
    if not user_choice_answers or not res["total"]:
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


def get_total_correct_match(first_column, second_column) -> List[List[str]]:
    res = []
    match_answers = MatchColumnMatchAnswer.objects.filter(first_content__isnull=False, second_content__isnull=False)
    match_answers_str = [[obj.first_content_id, obj.second_content_id] for obj in match_answers]

    for first_obj in first_column:
        for second_obj in second_column:
            if [first_obj.id, second_obj.id] in match_answers_str:
                res.append([str(first_obj.id), str(second_obj.id)])
            elif [second_obj.id, first_obj.id] in match_answers_str:
                res.append([str(second_obj.id), str(first_obj.id)])
    return res


def user_correct_quiz_match(user, course_id, lesson_id) -> List[Dict]:
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
            user=user,
            quiz__in=match_quiz,
        )
    )

    res = []
    for quiz in match_quiz:
        quiz_info = {"quiz_id": str(quiz.id), "user_answer": [], "correct_answer": [], "correct": 0, "total": 0}
        correct_match = get_total_correct_match(
            quiz.match_question.first_column.all(),
            quiz.match_question.second_column.all(),
        )
        quiz_info["correct_answer"].extend(correct_match)
        quiz_info["total"] = len(correct_match)
        for answer in user_match_answers.filter(quiz_id=quiz.id):
            first = str(answer.first_content_id)
            second = str(answer.second_content_id)
            if [first, second] in correct_match or [second, first] in correct_match:
                quiz_info["user_answer"].append([first, second])
                quiz_info["correct"] += 1
        res.append(quiz_info)

    return res


def quiz_statistic(user, course_id, lesson_id):
    choices_quiz = user_correct_quiz_choices(user, course_id, lesson_id)
    match_quiz = user_correct_quiz_match(user, course_id, lesson_id)
    valid_match_quiz = [quiz for quiz in match_quiz if quiz["total"]]

    res = {
        "mark": 0,
        "choices_quiz": choices_quiz,
        "match_quiz": match_quiz,
    }

    if not choices_quiz["total"] and not len(valid_match_quiz):
        return res

    mark_per_quiz = 10 / (choices_quiz["total"] + len(valid_match_quiz))
    total_mark = choices_quiz["correct"] + sum([quiz["correct"] / quiz["total"] for quiz in valid_match_quiz])
    res["mark"] = round(total_mark * mark_per_quiz, 2)

    return res


def response_quiz_statistic(quiz_statistic):
    config = Configuration.objects.first()

    if config and (not config.display_correct_answer or not config.display_mark):
        choices_quiz = quiz_statistic["choices_quiz"]
        match_quiz = quiz_statistic["match_quiz"]
        if not config.display_correct_answer:
            [result.pop("correct_answer", None) for result in choices_quiz["result"]]
            [obj.pop("correct_answer", None) for obj in match_quiz]
        if not config.display_mark:
            quiz_statistic.pop("mark", None)
            choices_quiz.pop("correct", None)
            [obj.pop("correct", None) for obj in match_quiz]

        quiz_statistic["choices_quiz"] = choices_quiz
        quiz_statistic["match_quiz"] = match_quiz

    return quiz_statistic


def quiz_data_processing(obj: Dict):
    obj_clone = obj.copy()

    if obj_clone.get("question_type") == QUESTION_TYPE_CHOICES:
        obj_clone.pop("match_question")
    elif obj_clone.get("question_type") == QUESTION_TYPE_MATCH:
        obj_clone.pop("choices_question")

    return obj_clone
