from django.db.models import Prefetch

from apps.quiz.models import (
    Quiz,
    QuestionManagement,
    MatchColumnContent,
    ChoicesAnswer,
    ChoicesQuestionUserAnswer,
)


def get_question_queryset():
    return QuestionManagement.objects.select_related(
            "choices_question__correct_answer",
            "match_question",
            "fill_blank_question",
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
                queryset=ChoicesAnswer.objects.select_related("answer_image", "choice_name")
            ),
        )


def get_quiz_queryset():
    return Quiz.objects.prefetch_related(
        Prefetch("question_mngt", queryset=get_question_queryset())
    )


def get_user_choice_answer_queryset(qs=None):
    res = qs if qs is not None else ChoicesQuestionUserAnswer.objects.all()
    return res.select_related(
            "user", "question", "choice",
        ).prefetch_related(
            Prefetch("question", queryset=get_question_queryset())
        )
