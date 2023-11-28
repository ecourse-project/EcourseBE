from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.conf import settings
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.courses.models import *
from apps.courses.forms import CourseForm
from apps.courses.services.admin_action import *
from apps.courses.services.admin import AdminCoursePermissons

from apps.upload.models import UploadFile
from apps.upload.enums import video_ext_list

from apps.core.general.init_data import UserDataManagementService
from apps.core.general.admin_site import get_admin_attrs

from apps.quiz.models import Quiz


@admin.register(CourseDocument)
class CourseDocumentAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseDocument", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseDocument", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "CourseDocument", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "CourseDocument", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "CourseDocument", "list_display")

    def get_form(self, request, obj=None, **kwargs):
        form = super(CourseDocumentAdmin, self).get_form(request, obj, **kwargs)
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        q_list = Q()
        for q in [Q(file_type__iexact=ext) for ext in video_ext_list]:
            q_list |= q
        form.base_fields['file'].queryset = UploadFile.objects.filter(~q_list & filter_condition)
        form.base_fields['topic'].queryset = CourseTopic.objects.filter(filter_condition)
        return form

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        return (
            super(CourseDocumentAdmin, self)
            .get_queryset(request)
            .select_related("topic", "author")
            .filter(filter_condition)
        )

    def save_model(self, request, obj, form, change):
        if not CourseDocument.objects.filter(pk=obj.id).exists():
            obj.author = request.user
        obj.save()


@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseTopic", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseTopic", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "CourseTopic", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "CourseTopic", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "CourseTopic", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        return (
            super(CourseTopicAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(filter_condition)
        )

    def save_model(self, request, obj, form, change):
        if not CourseTopic.objects.filter(pk=obj.id).exists():
            obj.author = request.user
        obj.save()


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
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "Lesson", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "Lesson", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "Lesson", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "Lesson", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "Lesson", "list_display")

    filter_horizontal = ("videos", "documents")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        filter_condition &= Q(removed=False)
        return (
            super(LessonAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(filter_condition)
        )

    # Query objects for many to many
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        if db_field.name == "videos":
            kwargs["queryset"] = UploadVideo.objects.filter(filter_condition)
        if db_field.name == "documents":
            kwargs["queryset"] = CourseDocument.objects.filter(filter_condition)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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

    def save_model(self, request, obj, form, change):
        if not Lesson.objects.filter(pk=obj.id).exists():
            obj.author = request.user
        obj.save()

    def save_related(self, request, form, formsets, change):
        instance = form.instance

        before_documents = set(instance.documents.all())
        before_videos = set(instance.videos.all())
        super().save_related(request, form, formsets, change)
        after_documents = set(instance.documents.all())
        after_videos = set(instance.videos.all())

        docs_remove = before_documents.difference(after_documents)
        videos_remove = before_videos.difference(after_videos)

        if docs_remove or videos_remove:
            if docs_remove:
                CourseDocumentManagement.objects.filter(lesson=instance, document__in=docs_remove).update(is_available=False)
            if videos_remove:
                VideoManagement.objects.filter(lesson=instance, video__in=videos_remove).update(is_available=False)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "Course", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "Course", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "Course", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "Course", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "Course", "list_display")

    ordering = ("name",)
    filter_horizontal = ("lessons",)
    form = CourseForm
    change_form_template = "admin_button/remove_lesson.html"

    def response_change(self, request, obj):
        if "remove-lesson" in request.POST:
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CourseAdmin, self).get_form(request, obj, **kwargs)
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        form.base_fields['topic'].queryset = CourseTopic.objects.filter(filter_condition)
        form.base_fields['lessons_remove'].queryset = Lesson.objects.filter(filter_condition & Q(removed=False))
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        filter_condition &= Q(removed=False)
        if db_field.name == "lessons":
            kwargs["queryset"] = Lesson.objects.filter(filter_condition)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).get_filter_condition()
        return (
            super(CourseAdmin, self)
            .get_queryset(request)
            .select_related('topic', 'author')
            .filter(filter_condition)
        )

    def save_model(self, request, obj, form, change):
        if obj.course_of_class:
            obj.is_selling = False
            obj.author = request.user
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


@admin.register(CourseManagement)
class CourseManagementAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseManagement", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseManagement", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "CourseManagement", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "CourseManagement", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "CourseManagement", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).get_filter_condition("course")
        return (
            super(CourseManagementAdmin, self)
            .get_queryset(request)
            .select_related("user", "course")
            .filter(filter_condition)
            .order_by("course")
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "CourseManagement", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "CourseManagement", "has_change_permission")


@admin.register(LessonManagement)
class LessonManagementAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "LessonManagement", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "LessonManagement", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "LessonManagement", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "LessonManagement", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "LessonManagement", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition_fk("course")
        return (
            super(LessonManagementAdmin, self)
            .get_queryset(request)
            .select_related("lesson", "course")
            .filter(filter_condition)
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "LessonManagement", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "LessonManagement", "has_change_permission")


@admin.register(CourseDocumentManagement)
class CourseDocumentManagementAdmin(admin.ModelAdmin):
    actions = (enable, disable)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseDocumentManagement", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "CourseDocumentManagement", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "CourseDocumentManagement", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "CourseDocumentManagement", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "CourseDocumentManagement", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition_fk("course")
        return (
            super(CourseDocumentManagementAdmin, self)
            .get_queryset(request)
            .select_related("document", "lesson", "course", "user")
            .filter(filter_condition)
            .order_by("course", "lesson", "document__order")
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "CourseDocumentManagement", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "CourseDocumentManagement", "has_change_permission")


@admin.register(VideoManagement)
class VideoManagementAdmin(admin.ModelAdmin):
    actions = (enable, disable)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "VideoManagement", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "VideoManagement", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "VideoManagement", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "VideoManagement", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "VideoManagement", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition_fk("course")
        return (
            super(VideoManagementAdmin, self)
            .get_queryset(request)
            .select_related("video", "lesson", "course", "user")
            .filter(filter_condition)
            .order_by("course", "lesson", "video__order")
        )

    def has_add_permission(self, request):
        return get_admin_attrs(request, "VideoManagement", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "VideoManagement", "has_change_permission")


@admin.register(QuizManagement)
class QuizManagementAdmin(admin.ModelAdmin, DynamicArrayMixin):
    change_form_template = "admin_button/clear_quiz.html"

    def quiz_author(self, obj):
        return obj.quiz.author.email if obj.quiz and obj.quiz.author else "-"

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "QuizManagement", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "QuizManagement", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "QuizManagement", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "QuizManagement", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "QuizManagement", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminCoursePermissons(request.user).user_condition_fk("course")
        return (
            super(QuizManagementAdmin, self)
            .get_queryset(request)
            .select_related("course", "lesson", "quiz", "user")
            .filter(filter_condition)
            .order_by("course", "lesson")
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        filter_condition = AdminCoursePermissons(request.user).user_condition()
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(filter_condition)
        if db_field.name == "lesson":
            kwargs["queryset"] = Lesson.objects.filter(filter_condition & Q(removed=False))
        if db_field.name == "quiz":
            kwargs["queryset"] = Quiz.objects.filter(filter_condition)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    def has_add_permission(self, request):
        return get_admin_attrs(request, "QuizManagement", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "QuizManagement", "has_change_permission")

