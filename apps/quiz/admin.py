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
    list_display = [
        'name',
        'id',
    ]


@admin.register(ChoicesAnswer)
class ChoicesAnswerAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "ChoicesAnswer", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "ChoicesAnswer", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "ChoicesAnswer", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "ChoicesAnswer", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(ChoicesAnswerAdmin, self)
            .get_queryset(request)
            .select_related("answer_image", "choice_name", "author")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "ChoicesAnswer", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "ChoicesAnswer", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "ChoicesAnswer", "has_delete_permission")


@admin.register(ChoicesQuestion)
class ChoicesQuestionAdmin(admin.ModelAdmin):
    def content_image_url(self, obj):
        if obj.content_image and obj.content_image.image_path:
            url = settings.BASE_URL + obj.content_image.image_path.url
            return format_html(f'<a href="{url}">{url}</a>')
        return ""

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "ChoicesQuestion", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "ChoicesQuestion", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "ChoicesQuestion", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "ChoicesQuestion", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(ChoicesQuestionAdmin, self)
            .get_queryset(request)
            .select_related("content_image", "correct_answer", "author")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "ChoicesQuestion", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "ChoicesQuestion", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "ChoicesQuestion", "has_delete_permission")


@admin.register(MatchColumnContent)
class MatchColumnContentAdmin(admin.ModelAdmin):
    def content_image_url(self, obj):
        if obj.content_image and obj.content_image.image_path:
            url = settings.BASE_URL + obj.content_image.image_path.url
            return format_html(f'<a href="{url}">{url}</a>')
        return ""

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnContent", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "MatchColumnContent", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "MatchColumnContent", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "MatchColumnContent", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(MatchColumnContentAdmin, self)
            .get_queryset(request)
            .select_related("content_image", "author")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "MatchColumnContent", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnContent", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnContent", "has_delete_permission")


@admin.register(MatchColumnMatchAnswer)
class MatchColumnMatchAnswerAdmin(admin.ModelAdmin):
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

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(MatchColumnMatchAnswerAdmin, self)
            .get_queryset(request)
            .select_related("match_question", "first_content", "second_content", "author")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnMatchAnswer", "has_delete_permission")


@admin.register(MatchColumnQuestion)
class MatchColumnQuestionAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnQuestion", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "MatchColumnQuestion", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "MatchColumnQuestion", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "MatchColumnQuestion", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(MatchColumnQuestionAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "MatchColumnQuestion", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnQuestion", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "MatchColumnQuestion", "has_delete_permission")


@admin.register(FillBlankQuestion)
class FillBlankQuestionAdmin(admin.ModelAdmin):
    form = FillBlankQuestionForm

    def original_content(self, obj):
        return get_summary_content(obj.content, 15)

    def display_content(self, obj):
        content = get_final_content(obj.content, obj.hidden_words, res_default=obj.content)
        return get_summary_content(content, 15)

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "FillBlankQuestion", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "FillBlankQuestion", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "FillBlankQuestion", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "FillBlankQuestion", "list_display")

    def save_model(self, request, obj, form, change):
        old_instance = FillBlankQuestion.objects.filter(pk=obj.pk).first()
        if (not obj.hidden_words and obj.content) or (old_instance and old_instance.content != obj.content):
            obj.hidden_words = split_content(obj.content)

        word_ids = form.cleaned_data.get("hidden")
        if obj.hidden_words and isinstance(word_ids, list):
            for word in obj.hidden_words:
                word["hidden"] = True if str(word.get("id")) in word_ids else False

        obj.save()

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition()
        return (
            super(FillBlankQuestionAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "FillBlankQuestion", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "FillBlankQuestion", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "FillBlankQuestion", "has_delete_permission")


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
        filter_condition = AdminQuizPermissons(request.user).user_condition("question__choices_question__author")
        return (
            get_user_choice_answer_queryset(
                super(ChoicesQuestionUserAnswerAdmin, self)
                .get_queryset(request)
                .filter(filter_condition)
            )
        )


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

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition("question__match_question__author")
        return (
            super(MatchColumnUserAnswerAdmin, self)
            .get_queryset(request)
            .select_related("user", "question", "first_content", "second_content")
            .filter(filter_condition)
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

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).user_condition("question__fill_blank_question__author")
        return (
            super(FillBlankUserAnswerAdmin, self)
            .get_queryset(request)
            .filter(filter_condition)
        )


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
        "author",
    )

    def author(self, obj):
        if obj.choices_question and obj.choices_question.author:
            return obj.choices_question.author.email
        elif obj.match_question and obj.match_question.author:
            return obj.match_question.author.email
        elif obj.fill_blank_question and obj.fill_blank_question.author:
            return obj.fill_blank_question.author.email
        return "-"

    def get_fields(self, request, obj=None):
        fields = super(QuestionManagementAdmin, self).get_fields(request, obj)
        return fields

    def get_queryset(self, request):
        filter_condition = AdminQuizPermissons(request.user).question_mngt_user_condition()
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
            .filter(filter_condition)
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

    def has_add_permission(self, request):
        return get_admin_attrs(request, "Quiz", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "Quiz", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "Quiz", "has_delete_permission")
