from django.contrib import admin
from django.http import HttpResponseRedirect

from apps.core.utils import get_summary_content
from apps.quiz.models import (
    ChoicesQuizChoiceName,
    ChoicesQuizAnswer,
    ChoicesQuizQuestion,
    MatchColumnContent,
    MatchColumnMatchAnswer,
    MatchColumnQuestion,
    FillBlankQuestion,
    MatchColumnUserAnswer,
    ChoicesQuizUserAnswer,
    QuizManagement,
)
from apps.quiz.forms import FillBlankQuestionForm, QuizManagementForm
from apps.quiz.services.fill_blank_services import split_content, get_final_content


@admin.register(ChoicesQuizChoiceName)
class ChoicesQuizChoiceNameAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(ChoicesQuizAnswer)
class ChoicesQuizAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'answer_text',
        'answer_type',
        'choice_name',
    )

    def get_queryset(self, request):
        return super(ChoicesQuizAnswerAdmin, self).get_queryset(request).select_related("answer_image", "choice_name")


@admin.register(ChoicesQuizQuestion)
class ChoicesQuizQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'content_text',
        'content_image',
        'content_type',
        'correct_answer',
    )

    def get_queryset(self, request):
        return super(ChoicesQuizQuestionAdmin, self).get_queryset(request).select_related("course", "correct_answer")


@admin.register(QuizManagement)
class QuizManagementAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'choices_question',
        'course',
    )
    form = QuizManagementForm

    def get_queryset(self, request):
        return super(QuizManagementAdmin, self).get_queryset(request).select_related("choices_question", "course")


@admin.register(ChoicesQuizUserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'choice',
    )

    def get_queryset(self, request):
        return super(UserAnswerAdmin, self).get_queryset(request).select_related("user", "quiz")


@admin.register(MatchColumnContent)
class MatchColumnContentAdmin(admin.ModelAdmin):
    list_display = (
        'content_text',
        'content_image',
        'content_type',
    )


@admin.register(MatchColumnMatchAnswer)
class MatchColumnMatchAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'first_content',
        'second_content',
    )


@admin.register(MatchColumnQuestion)
class MatchColumnQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'content',
    )


@admin.register(FillBlankQuestion)
class FillBlankQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'original_content',
        'display_content',
    )
    form = FillBlankQuestionForm
    readonly_fields = ("hidden_words",)

    def original_content(self, obj):
        return get_summary_content(obj.content, 15)

    def display_content(self, obj):
        content = get_final_content(obj.hidden_words, res_default=obj.content)
        return get_summary_content(content, 15)

    def save_model(self, request, obj, form, change):
        old_instance = FillBlankQuestion.objects.filter(pk=obj.pk).first()
        if (not obj.hidden_words and obj.content) or (old_instance and old_instance.content != obj.content):
            obj.hidden_words = split_content(obj.content)

        word_ids = form.cleaned_data.get("hidden")
        if obj.hidden_words and isinstance(word_ids, list):
            for word in obj.hidden_words:
                word["hidden"] = True if str(word.get("id")) in word_ids else False

        obj.save()


@admin.register(MatchColumnUserAnswer)
class MatchColumnUserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'answer',
    )

    def answer(self, obj):
        return (
            f"{get_summary_content(obj.first_content.content_text)} - {get_summary_content(obj.second_content.content_text)}"
        )