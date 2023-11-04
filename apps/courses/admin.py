from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.conf import settings
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.courses.models import *
from apps.courses.forms import CourseForm
from apps.courses.services.admin_action import *

from apps.upload.models import UploadFile
from apps.upload.enums import video_ext_list

from apps.core.general.init_data import UserDataManagementService


@admin.register(CourseDocument)
class CourseDocumentAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "topic__name",
    )
    list_display = (
        "name",
        "topic",
    )
    list_filter = (
        "topic",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(CourseDocumentAdmin, self).get_form(request, obj, **kwargs)
        q_list = Q()
        for q in [Q(file_type__iexact=ext) for ext in video_ext_list]:
            q_list |= q
        form.base_fields['file'].queryset = UploadFile.objects.filter(~q_list)
        return form

    def get_queryset(self, request):
        return super(CourseDocumentAdmin, self).get_queryset(request).prefetch_related("topic")


@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


@admin.register(LessonsRemoved)
class LessonsRemovedAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "lesson_number",
    )
    actions = (unremove,)

    def get_queryset(self, request):
        qs = super(LessonsRemovedAdmin, self).get_queryset(request)
        return qs.filter(removed=True)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    list_display = (
        "name",
        "lesson_number",
        "course_include",
        "class_include",
        "id",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("total_documents", "total_videos")
    filter_horizontal = ("videos", "documents")

    def get_queryset(self, request):
        qs = super(LessonAdmin, self).get_queryset(request)
        return qs.filter(removed=False)

    def get_fields(self, request, obj=None):
        fields = super(LessonAdmin, self).get_fields(request, obj)
        removed_fields = ["total_documents", "total_videos"]
        if not request.user.is_superuser:
            removed_fields.extend(["removed"])
        for field in removed_fields:
            fields.remove(field)
        return fields

    def course_include(self, obj):
        courses = obj.courses.filter(course_of_class=False).values_list(*["id", "name"])
        html_res = [
            f'<a href="{settings.BASE_URL}/admin/courses/course/{item[0]}/change/">{item[1]}</a>'
            for item in courses
        ]
        return format_html("<br>".join([res for res in html_res]))

    def class_include(self, obj):
        classes = obj.courses.filter(course_of_class=True).values_list(*["id", "name"])
        html_res = [
            f'<a href="{settings.BASE_URL}/admin/classes/class/{item[0]}/change/">{item[1]}</a>'
            for item in classes
        ]
        return format_html("<br>".join([res for res in html_res]))

    def save_related(self, request, form, formsets, change):
        instance = form.instance

        before_documents = set(instance.documents.all())
        before_videos = set(instance.videos.all())
        super().save_related(request, form, formsets, change)
        after_documents = set(instance.documents.all())
        after_videos = set(instance.videos.all())

        # docs_add = after_documents.difference(before_documents)
        # videos_add = after_videos.difference(before_videos)
        docs_remove = before_documents.difference(after_documents)
        videos_remove = before_videos.difference(after_videos)

        if docs_remove or videos_remove:
            if docs_remove:
                CourseDocumentManagement.objects.filter(lesson=instance, document__in=docs_remove).update(is_available=False)
            if videos_remove:
                VideoManagement.objects.filter(lesson=instance, video__in=videos_remove).update(is_available=False)

    # Query objects for many to many
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     # if db_field.name == "documents":
    #     #     kwargs["queryset"] = CourseDocument.objects.exclude(
    #     #         id__in=Lesson.documents.through.objects.all().values_list('coursedocument_id', flat=True)
    #     #     )
    #
    #     if db_field.name == "videos":
    #         q_list = Q()
    #         for q in [Q(file_type__iexact=ext) for ext in video_ext_list]:
    #             q_list |= q
    #         kwargs["queryset"] = UploadFile.objects.filter(q_list)
    #         # kwargs["queryset"] = UploadFile.objects.filter(file_type__iexact="mov")
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name", "topic", "is_selling")
    search_fields = (
        "id",
        "name",
    )
    list_display = (
        "name",
        "topic",
        "price",
        "is_selling",
        "created",
        "id",
    )
    ordering = (
        "name",
    )
    filter_horizontal = ("lessons",)
    form = CourseForm
    change_form_template = "admin_button/remove_lesson.html"

    def get_fields(self, request, obj=None):
        fields = super(CourseAdmin, self).get_fields(request, obj)
        removed_fields = []
        if not request.user.is_superuser:
            removed_fields.extend(["test", "init_data", "structure"])
        for field in removed_fields:
            fields.remove(field)
        return fields

    def response_change(self, request, obj):
        if "remove-lesson" in request.POST:
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def save_model(self, request, obj, form, change):
        if obj.course_of_class:
            obj.is_selling = False
        obj.save()

    def save_related(self, request, form, formsets, change):
        instance = form.instance
        before_lessons = set(instance.lessons.all())
        super().save_related(request, form, formsets, change)
        after_lessons = set(instance.lessons.all())

        all_lessons = instance.lessons.all()
        lessons_remove = before_lessons.difference(after_lessons)
        lessons_add = after_lessons.difference(before_lessons)

        if not instance.init_data:
            UserDataManagementService(None).create_lesson_mngt(instance, all_lessons)
            UserDataManagementService(None).create_course_mngt_for_multiple_users(instance)
            instance.init_data = True
            instance.save(update_fields=["init_data"])
        else:
            if lessons_add:
                UserDataManagementService(None).create_lesson_mngt(instance, all_lessons)
                CourseDocumentManagement.objects.filter(course=instance, lesson__in=lessons_add).update(is_available=True)
                VideoManagement.objects.filter(course=instance, lesson__in=lessons_add).update(is_available=True)
            if lessons_remove:
                LessonManagement.objects.filter(course=instance, lesson__in=lessons_remove).delete()
                CourseDocumentManagement.objects.filter(course=instance, lesson__in=lessons_remove).update(is_available=False)
                VideoManagement.objects.filter(course=instance, lesson__in=lessons_remove).update(is_available=False)

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request).prefetch_related("lessons").select_related('topic')
        return qs.filter(course_of_class=False)


@admin.register(CourseManagement)
class CourseManagementAdmin(admin.ModelAdmin):
    list_filter = ("course__course_of_class", "course", "sale_status")
    search_fields = (
        "course__name",
        "sale_status",
        "user__email",
    )
    list_display = (
        "user",
        "course",
        "progress",
        "mark",
        "is_done_quiz",
        "sale_status",
        "views",
    )
    readonly_fields = ("progress", "user_in_class", "views")

    def get_queryset(self, request):
        qs_condition = Q(course__course_of_class=False)
        return (
            super(CourseManagementAdmin, self)
            .get_queryset(request)
            .select_related("user", "course")
            .filter(qs_condition)
            .order_by("course")
        )

    def get_fields(self, request, obj=None):
        fields = super(CourseManagementAdmin, self).get_fields(request, obj)
        remove_fields = ["is_favorite"]
        if not request.user.is_superuser:
            remove_fields.extend(["views"])
        for field in remove_fields:
            fields.remove(field)
        return fields

    def get_list_display(self, request):
        list_display = super(CourseManagementAdmin, self).get_list_display(request)
        if not request.user.is_superuser:
            list_display = list(list_display)
            list_display.remove("views")
            return tuple(list_display)
        return list_display


@admin.register(LessonManagement)
class LessonManagementAdmin(admin.ModelAdmin):
    list_filter = ("course",)
    search_fields = (
        "course__name",
    )
    list_display = (
        "course",
        "lesson",
    )

    def get_queryset(self, request):
        return (
            super(LessonManagementAdmin, self)
            .get_queryset(request)
            .select_related("lesson", "course")
        )


@admin.register(CourseDocumentManagement)
class CourseDocumentManagementAdmin(admin.ModelAdmin):
    list_filter = ("course",)
    search_fields = (
        "user__email",
        "course__name",
    )
    list_display = (
        "user",
        "course",
        "lesson",
        "document",
        "is_completed",
        "is_available",
        "enable"
    )
    actions = (enable, disable)
    readonly_fields = ("is_available",)

    def get_queryset(self, request):
        return (
            super(CourseDocumentManagementAdmin, self)
            .get_queryset(request)
            .select_related("document", "lesson", "course", "user")
            .order_by("course", "lesson", "document__order")
        )


@admin.register(VideoManagement)
class VideoManagementAdmin(admin.ModelAdmin):
    list_filter = ("course",)
    search_fields = (
        "user__email",
        "course__name",
    )
    list_display = (
        "user",
        "course",
        "lesson",
        "video",
        "is_completed",
        "is_available",
        "enable",
    )
    actions = (enable, disable)

    def get_queryset(self, request):
        return (
            super(VideoManagementAdmin, self)
            .get_queryset(request)
            .select_related("video", "lesson", "course", "user")
            .order_by("course", "lesson", "video__order")
        )


@admin.register(QuizManagement)
class QuizManagementAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        "user",
        "course",
        "lesson",
        "quiz",
        "is_done_quiz",
        "date_done_quiz",
    )
    fields = (
        "user",
        "course",
        "lesson",
        "quiz",
        "is_done_quiz",
        "date_done_quiz",
        "start_time",
        "history",
    )
    change_form_template = "admin_button/clear_quiz.html"
    readonly_fields = ("course", "lesson", "quiz", "user")

    # def get_fields(self, request, obj=None):
    #     fields = super(LessonQuizManagementAdmin, self).get_fields(request, obj)
    #     for field in ["course_mngt"]:
    #         fields.remove(field)
    #     print(fields)
    #     return fields

    def get_queryset(self, request):
        return (
            super(QuizManagementAdmin, self)
            .get_queryset(request)
            .select_related("course", "lesson", "quiz", "user")
            .order_by("course", "lesson")
        )

    def response_change(self, request, obj):
        if "clear-quiz" in request.POST:
            history = obj.history or []
            if obj.date_done_quiz:
                history.append(obj.date_done_quiz.isoformat())
            obj.history = history
            obj.is_done_quiz = False
            obj.date_done_quiz = None
            obj.start_time = None
            obj.save(update_fields=["history", "is_done_quiz", "date_done_quiz", "start_time"])
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

