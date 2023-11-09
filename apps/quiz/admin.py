from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings


from apps.core.general.admin_site import get_admin_attrs
from apps.quiz.models import *
from apps.quiz.forms import FillBlankQuestionForm
from apps.quiz.services.fill_blank_services import split_content, get_final_content
from apps.quiz.services.queryset_services import get_user_choice_answer_queryset
from apps.quiz.services.admin import AdminQuizPermissons
from apps.quiz.enums import ANSWER_TYPE_TEXT, ANSWER_TYPE_IMAGE


@admin.register(ChoiceName)
class ChoiceNameAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(ChoicesAnswer)
class ChoicesAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'answer_text',
        'answer_type',
        'choice_name',
        "id",
    )

    def get_queryset(self, request):
        return super(ChoicesAnswerAdmin, self).get_queryset(request).select_related("answer_image", "choice_name")


@admin.register(ChoicesQuestion)
class ChoicesQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'content_text',
        'content_image_url',
        'content_type',
        'correct_answer',
        "id",
    )

    def get_queryset(self, request):
        return super(ChoicesQuestionAdmin, self).get_queryset(request).select_related("content_image", "correct_answer")

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
        "id",
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
        'match_question',
        'first',
        'second',
        "id",
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
        "id",
    )

    def get_queryset(self, request):
        return super(MatchColumnQuestionAdmin, self).get_queryset(request)


@admin.register(FillBlankQuestion)
class FillBlankQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'original_content',
        'display_content',
        "id",
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


@admin.register(ChoicesQuestionUserAnswer)
class ChoicesQuestionUserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'choice',
        'created',
        "id",
    )
    readonly_fields = ('created',)

    def get_queryset(self, request):
        return get_user_choice_answer_queryset(super(ChoicesQuestionUserAnswerAdmin, self).get_queryset(request))


@admin.register(MatchColumnUserAnswer)
class MatchColumnUserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'answer',
        'created',
        "id",
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
        'question',
        'words',
        'created',
        "id",
    )
    readonly_fields = ('created',)


@admin.register(QuestionManagement)
class QuestionManagementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'order',
        'question_type',
        'choices_question',
        'match_question',
        'fill_blank_question',
        "time_limit",
    )

    def get_fields(self, request, obj=None):
        fields = super(QuestionManagementAdmin, self).get_fields(request, obj)
        return fields

    def get_queryset(self, request):
        return (
            super(QuestionManagementAdmin, self).get_queryset(request)
            .only(
                "id",
                "order",
                "question_type",
                "choices_question",
                "match_question",
                "fill_blank_question",
                "time_limit",
            )
            .defer(
                "created",
                "modified",
                "choices_question_id",
                "choices_question__created",
                "choices_question__modified",
                "match_question_id",
                "match_question__created",
                "match_question__modified",
                "fill_blank_question_id",
                "fill_blank_question__created",
                "fill_blank_question__modified",
            )
            .select_related(
                "choices_question",
                "match_question",
                "fill_blank_question",
            )
        )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "Quiz", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "Quiz", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "Quiz", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "Quiz", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "Quiz", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(QuizAdmin, self)
            .get_queryset(request)
            .select_related('author')
            .filter(filter_condition)
        )
