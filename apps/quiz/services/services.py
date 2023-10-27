from typing import Text, Dict, List, Union

from apps.quiz.enums import (
    QUESTION_TYPE_CHOICES,
    QUESTION_TYPE_MATCH,
    QUESTION_TYPE_FILL,
)
from apps.quiz.models import (
    QuizManagement,
    ChoicesQuizUserAnswer,
    MatchColumnUserAnswer,
    FillBlankUserAnswer,
)
from apps.quiz.services.choices_question_services import (
    user_correct_quiz_choices,
    store_choices_question,
    delete_choices_question,
)
from apps.quiz.services.match_column_services import (
    user_correct_quiz_match,
    store_match_question,
    delete_match_question,
)
from apps.quiz.services.fill_blank_services import (
    user_correct_quiz_fill,
    store_fill_question,
    delete_fill_question,
)
from apps.configuration.models import Configuration
from apps.courses.models import LessonManagement, CourseManagement
from apps.core.utils import get_now


def store_quiz(data: Dict):
    choices_ques_mngt = store_choices_question(data.get("choices_question", []))
    match_ques_mngt = store_match_question(data.get("match_question", []))
    fill_ques_mngt = store_fill_question(data.get("fill_blank_question", []))

    all_obj = []
    for lst_obj in [choices_ques_mngt, match_ques_mngt, fill_ques_mngt]:
        for obj in lst_obj:
            obj.name = data.get("name")
            obj.lesson_id = data.get("lesson_id")
            obj.course_id = data.get("course_id")
        all_obj.extend(lst_obj)

    if all_obj:
        return QuizManagement.objects.bulk_create(all_obj)
    return QuizManagement.objects.none()


def delete_quiz(list_question_id: Union[List[Text], Text]):
    list_id = [list_question_id] if isinstance(list_question_id, Text) else list_question_id
    for item in list_id:
        quiz_mngt = QuizManagement.objects.filter(pk=item).first()
        if quiz_mngt:
            if quiz_mngt.question_type == QUESTION_TYPE_CHOICES:
                delete_choices_question(quiz_mngt)
            elif quiz_mngt.question_type == QUESTION_TYPE_MATCH:
                delete_match_question(quiz_mngt)
            elif quiz_mngt.question_type == QUESTION_TYPE_FILL:
                delete_fill_question(quiz_mngt)


def edit_quiz(data: Dict):
    choices_ques = data.get("choices_question", [])
    match_ques = data.get("match_question", [])
    fill_ques = data.get("fill_blank_question", [])

    list_ques_id = [
        obj.get("id")
        for list_ques in [choices_ques, match_ques, fill_ques]
        for obj in list_ques
        if obj.get("id")
    ]

    delete_quiz(list_ques_id)
    new_quiz = store_quiz(data)
    return new_quiz


def store_user_answers(user, user_answers):
    choice_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_CHOICES]
    match_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_MATCH]
    fill_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_FILL]
    now = get_now()

    choice_answer_objs = [
        ChoicesQuizUserAnswer(
            created=now,
            user=user,
            quiz_id=choice_obj.get("quiz_id"),
            choice_id=choice_obj.get("answer"),
        )
        for choice_obj in choice_type_objs
    ]

    match_answer_objs = [
        MatchColumnUserAnswer(
            created=now,
            user=user,
            quiz_id=match_obj.get("quiz_id"),
            first_content_id=answer[0],
            second_content_id=answer[1],
        )
        for match_obj in match_type_objs
        for answer in match_obj.get("answer")
    ]

    fill_answer_objs = [
        FillBlankUserAnswer(
            created=now,
            user=user,
            quiz_id=fill_obj.get("quiz_id"),
            words=fill_obj.get("answer") or [],
        )
        for fill_obj in fill_type_objs
    ]

    if choice_answer_objs:
        ChoicesQuizUserAnswer.objects.bulk_create(choice_answer_objs)
    if match_answer_objs:
        MatchColumnUserAnswer.objects.bulk_create(match_answer_objs)
    if fill_answer_objs:
        FillBlankUserAnswer.objects.bulk_create(fill_answer_objs)

    return now, choice_answer_objs, match_answer_objs, fill_answer_objs


def quiz_statistic(user, course_id, lesson_id, created):
    choices_quiz = user_correct_quiz_choices(user, course_id, lesson_id, created)
    match_quiz = user_correct_quiz_match(user, course_id, lesson_id, created)
    fill_quiz = user_correct_quiz_fill(user, course_id, lesson_id, created)
    valid_match_quiz = [quiz for quiz in match_quiz if quiz["total"]]
    valid_fill_quiz = [quiz for quiz in fill_quiz if quiz["total"]]

    res = {
        "mark": 0,
        "choices_quiz": choices_quiz,
        "match_quiz": match_quiz,
        "fill_quiz": fill_quiz,
    }

    if not choices_quiz["total"] and not len(valid_match_quiz) and not len(valid_fill_quiz):
        return res

    # mark_per_quiz = 10 / (choices_quiz["total"] + len(valid_match_quiz) + len(valid_fill_quiz))
    total_quiz = choices_quiz["total"] + len(valid_match_quiz) + len(valid_fill_quiz)
    total_correct = (
        choices_quiz["correct"]
        + len([1 for quiz in valid_match_quiz if quiz["correct"] == quiz["total"]])
        + len([1 for quiz in valid_fill_quiz if quiz["correct"] == quiz["total"]])
    )

    res["mark"] = round(100 * total_correct / total_quiz, 0)

    return res


def response_quiz_statistic(quiz_statistic_data):
    config = Configuration.objects.first()

    if config and (not config.display_correct_answer or not config.display_mark):
        choices_quiz = quiz_statistic_data["choices_quiz"]
        match_quiz = quiz_statistic_data["match_quiz"]
        fill_quiz = quiz_statistic_data["fill_quiz"]
        if not config.display_correct_answer:
            [result.pop("correct_answer", None) for result in choices_quiz["result"]]
            [obj.pop("correct_answer", None) for obj in match_quiz]
            [obj.pop("correct_answer", None) for obj in fill_quiz]
        if not config.display_mark:
            quiz_statistic_data.pop("mark", None)
            choices_quiz.pop("correct", None)
            [obj.pop("correct", None) for obj in match_quiz]
            [obj.pop("correct", None) for obj in fill_quiz]

        quiz_statistic_data["choices_quiz"] = choices_quiz
        quiz_statistic_data["match_quiz"] = match_quiz
        quiz_statistic_data["fill_quiz"] = fill_quiz

    return quiz_statistic_data


def quiz_data_processing(obj: Dict):
    obj_clone = obj.copy()

    if obj_clone.get("question_type") == QUESTION_TYPE_CHOICES:
        obj_clone.pop("match_question")
        obj_clone.pop("fill_blank_question")
    elif obj_clone.get("question_type") == QUESTION_TYPE_MATCH:
        obj_clone.pop("choices_question")
        obj_clone.pop("fill_blank_question")
    elif obj_clone.get("question_type") == QUESTION_TYPE_FILL:
        obj_clone.pop("choices_question")
        obj_clone.pop("match_question")

    return obj_clone


def validate_lesson_of_course(user, lesson_id, course_id):
    course_mngt = CourseManagement.objects.filter(course_id=course_id, user=user).first()
    lesson_quiz_mngt = LessonManagement.objects.filter(course_id=course_id, lesson_id=lesson_id).first()
    return course_mngt if course_mngt and lesson_quiz_mngt else CourseManagement.objects.none()
