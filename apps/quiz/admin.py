from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.conf import settings

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
    FillBlankUserAnswer,
    QuizManagement,
)
from apps.quiz.forms import FillBlankQuestionForm, QuizManagementForm
from apps.quiz.services.fill_blank_services import split_content, get_final_content
from apps.quiz.services.services import get_user_choice_answer_queryset
from apps.quiz.enums import ANSWER_TYPE_TEXT, ANSWER_TYPE_IMAGE


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
        'content_image_url',
        'content_type',
        'correct_answer',
    )

    def get_queryset(self, request):
        return super(ChoicesQuizQuestionAdmin, self).get_queryset(request).select_related("content_image", "correct_answer")

    def content_image_url(self, obj):
        if obj.content_image and obj.content_image.image_path:
            url = settings.BASE_URL + obj.content_image.image_path.url
            return format_html(f'<a href="{url}">{url}</a>')
        return ""


@admin.register(MatchColumnContent)
class MatchColumnContentAdmin(admin.ModelAdmin):
    list_display = (
        'content_text',
        'content_image_url',
        'content_type',
    )

    def get_queryset(self, request):
        return super(MatchColumnContentAdmin, self).get_queryset(request).select_related("content_image")

    def content_image_url(self, obj):
        if obj.content_image and obj.content_image.image_path:
            url = settings.BASE_URL + obj.content_image.image_path.url
            return format_html(f'<a href="{url}">{url}</a>')
        return ""


@admin.register(MatchColumnMatchAnswer)
class MatchColumnMatchAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'first',
        'second',
    )

    def get_queryset(self, request):
        return super(MatchColumnMatchAnswerAdmin, self).get_queryset(request).select_related("first_content", "second_content")

    @staticmethod
    def display_content(input_content):
        if input_content and input_content.content_type == ANSWER_TYPE_TEXT:
            return get_summary_content(input_content.content_text)
        elif input_content and input_content.content_type == ANSWER_TYPE_IMAGE:
            if input_content.content_image and input_content.content_image.image_path:
                url = settings.BASE_URL + input_content.content_image.image_path.url
                return format_html(f'<a href="{url}">{url}</a>')
        return ""

    def first(self, obj):
        return self.display_content(obj.first_content)

    def second(self, obj):
        return self.display_content(obj.second_content)


@admin.register(MatchColumnQuestion)
class MatchColumnQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'content',
    )

    def get_queryset(self, request):
        return super(MatchColumnQuestionAdmin, self).get_queryset(request)


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


@admin.register(ChoicesQuizUserAnswer)
class ChoicesQuizUserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'choice',
        'created',
    )
    readonly_fields = ('created',)

    def get_queryset(self, request):
        return get_user_choice_answer_queryset(super(ChoicesQuizUserAnswerAdmin, self).get_queryset(request))


@admin.register(MatchColumnUserAnswer)
class MatchColumnUserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'answer',
        'created',
    )
    readonly_fields = ('created',)

    def answer(self, obj):
        return (
            f"{get_summary_content(obj.first_content.content_text)} - {get_summary_content(obj.second_content.content_text)}"
        )


@admin.register(FillBlankUserAnswer)
class FillBlankUserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'words',
        'created',
    )
    readonly_fields = ('created',)


@admin.register(QuizManagement)
class QuizManagementAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'course',
        'lesson',
        'question_type',
        'choices_question',
        'match_question',
        'fill_blank_question',
    )
    form = QuizManagementForm

    def get_queryset(self, request):
        return super(QuizManagementAdmin, self).get_queryset(request).select_related("choices_question", "course")