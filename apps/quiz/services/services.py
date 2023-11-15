from typing import Text, Dict, List, Union

from apps.quiz.enums import (
    QUESTION_TYPE_CHOICES,
    QUESTION_TYPE_MATCH,
    QUESTION_TYPE_FILL,
)
from apps.quiz.models import (
    Quiz,
    QuestionManagement,
    ChoicesQuestionUserAnswer,
    MatchColumnUserAnswer,
    FillBlankUserAnswer,
)
from apps.quiz.services.choices_question_services import (
    user_correct_question_choices,
    store_choices_question,
    delete_choices_question,
)
from apps.quiz.services.match_column_services import (
    user_correct_question_match,
    store_match_question,
    delete_match_question,
)
from apps.quiz.services.fill_blank_services import (
    user_correct_question_fill,
    store_fill_question,
    delete_fill_question,
)
from apps.quiz.exceptions import QuizDoesNotExistException
from apps.configuration.models import Configuration
from apps.courses.models import Course, Lesson
from apps.core.utils import get_now


def add_quiz(data: Dict, user):
    name = data.get("name")
    quiz = Quiz.objects.create(name=name, author=user)
    return quiz


def delete_quiz(quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = quiz.question_mngt.all()
        delete_question([ques.id for ques in questions])
        quiz.delete()
    except Quiz.DoesNotExist:
        raise QuizDoesNotExistException()


def assign_quiz(data: Dict):
    quiz_location = data.get("quiz_location")
    course_id = data.get("course_id")

    if not quiz_location:
        return {}

    course = Course.objects.get(pk=course_id)
    lessons = list(course.lessons.all())
    for lesson in lessons:
        lesson_id = str(lesson.pk)
        for obj in quiz_location:
            if lesson_id == obj["lesson_id"] and obj.get("quiz"):
                lesson.quiz_location = obj["quiz"]
                break

    Lesson.objects.bulk_update(lessons, fields=["quiz_location"])
    return {}


def store_question(data: List):
    choices_ques = [obj for obj in data if obj.get("question_type") == QUESTION_TYPE_CHOICES]
    match_ques = [obj for obj in data if obj.get("question_type") == QUESTION_TYPE_MATCH]
    fill_ques = [obj for obj in data if obj.get("question_type") == QUESTION_TYPE_FILL]

    choices_ques_mngt = store_choices_question(choices_ques)
    match_ques_mngt = store_match_question(match_ques)
    fill_ques_mngt = store_fill_question(fill_ques)

    all_obj = choices_ques_mngt + match_ques_mngt + fill_ques_mngt
    if all_obj:
        return QuestionManagement.objects.bulk_create(all_obj)
    return all_obj


def delete_question(list_question_id: Union[List[Text], Text]):
    list_id = [list_question_id] if isinstance(list_question_id, Text) else list_question_id
    list_question_mngt = QuestionManagement.objects.filter(pk__in=list_id)
    for question_mngt in list_question_mngt:
        if question_mngt.question_type == QUESTION_TYPE_CHOICES:
            delete_choices_question(question_mngt)
        elif question_mngt.question_type == QUESTION_TYPE_MATCH:
            delete_match_question(question_mngt)
        elif question_mngt.question_type == QUESTION_TYPE_FILL:
            delete_fill_question(question_mngt)


def edit_question(data: Dict):
    choices_ques = data.get("choices_question", [])
    match_ques = data.get("match_question", [])
    fill_ques = data.get("fill_blank_question", [])

    list_ques_id = [
        obj.get("id")
        for list_ques in [choices_ques, match_ques, fill_ques]
        for obj in list_ques
        if obj.get("id")
    ]

    delete_question(list_ques_id)
    # TODO Need edit line below
    new_question = edit_question(data)
    return new_question


def store_user_answers(user, user_answers):
    choice_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_CHOICES]
    match_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_MATCH]
    fill_type_objs = [obj for obj in user_answers if obj.get("question_type") == QUESTION_TYPE_FILL]
    now = get_now()

    choice_answer_objs = [
        ChoicesQuestionUserAnswer(
            created=now,
            user=user,
            question_id=choice_obj.get("question_id"),
            choice_id=choice_obj.get("answer"),
        )
        for choice_obj in choice_type_objs
    ]

    match_answer_objs = [
        MatchColumnUserAnswer(
            created=now,
            user=user,
            question_id=match_obj.get("question_id"),
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
            question_id=fill_obj.get("question_id"),
            words=fill_obj.get("answer") or [],
        )
        for fill_obj in fill_type_objs
    ]

    if choice_answer_objs:
        ChoicesQuestionUserAnswer.objects.bulk_create(choice_answer_objs)
    if match_answer_objs:
        MatchColumnUserAnswer.objects.bulk_create(match_answer_objs)
    if fill_answer_objs:
        FillBlankUserAnswer.objects.bulk_create(fill_answer_objs)

    return now, choice_answer_objs, match_answer_objs, fill_answer_objs


def quiz_statistic(quiz_id, user, created):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise QuizDoesNotExistException
    choices_question = user_correct_question_choices(quiz, user, created)
    match_question = user_correct_question_match(quiz, user, created)
    fill_question = user_correct_question_fill(quiz, user, created)
    valid_match_question = [question for question in match_question if question["total"]]
    valid_fill_question = [question for question in fill_question if question["total"]]

    res = {
        "id": quiz_id,
        "name": quiz.name,
        "mark": 0,
        "choices_question": choices_question,
        "match_question": match_question,
        "fill_question": fill_question,
    }

    if not choices_question["total"] and not len(valid_match_question) and not len(valid_fill_question):
        return res

    total_question = choices_question["total"] + len(valid_match_question) + len(valid_fill_question)
    total_correct = (
            choices_question["correct"]
            + len([1 for question in valid_match_question if question["correct"] == question["total"]])
            + len([1 for question in valid_fill_question if question["correct"] == question["total"]])
    )

    res["mark"] = round(100 * total_correct / total_question, 0)

    return res


def response_quiz_statistic(quiz_statistic_data):
    config = Configuration.objects.first()

    if config and (not config.display_correct_answer or not config.display_mark):
        choices_question = quiz_statistic_data["choices_question"]
        match_question = quiz_statistic_data["match_question"]
        fill_question = quiz_statistic_data["fill_question"]
        if not config.display_correct_answer:
            [result.pop("correct_answer", None) for result in choices_question["result"]]
            [obj.pop("correct_answer", None) for obj in match_question]
            [obj.pop("correct_answer", None) for obj in fill_question]
        if not config.display_mark:
            quiz_statistic_data.pop("mark", None)
            choices_question.pop("correct", None)
            [obj.pop("correct", None) for obj in match_question]
            [obj.pop("correct", None) for obj in fill_question]

        quiz_statistic_data["choices_quiz"] = choices_question
        quiz_statistic_data["match_quiz"] = match_question
        quiz_statistic_data["fill_quiz"] = fill_question

    return quiz_statistic_data


def question_data_processing(obj: Dict):
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
