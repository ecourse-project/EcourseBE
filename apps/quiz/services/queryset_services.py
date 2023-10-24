from django.db.models import Prefetch

from apps.quiz.models import (
    QuizManagement,
    MatchColumnContent,
    ChoicesQuizAnswer,
    ChoicesQuizUserAnswer,
)


def get_quiz_queryset():
    return QuizManagement.objects.select_related(
            "course",
            "choices_question",
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