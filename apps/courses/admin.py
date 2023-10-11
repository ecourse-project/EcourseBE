from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from django.conf import settings

from apps.courses.models import (
    Course,
    Lesson,
    CourseTopic,
    CourseDocument,
    LessonManagement,
    CourseManagement,
    CourseDocumentManagement,
    VideoManagement,
    LessonQuizManagement,
)
from apps.courses.services.admin import (
    insert_remove_docs_videos,
)
from apps.upload.models import UploadFile
from apps.upload.enums import video_ext_list


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
    )
    ordering = (
        "name",
    )
    readonly_fields = ("total_documents", "total_videos")
    filter_horizontal = ("videos", "documents")

    def get_fields(self, request, obj=None):
        fields = super(LessonAdmin, self).get_fields(request, obj)
        for field in ["total_documents", "total_videos"]:
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

        insert_remove_docs_videos(
            course_id=None,
            lesson_id=instance.id,
            docs_remove=before_documents.difference(after_documents),
            videos_remove=before_videos.difference(after_videos),
            docs_add=after_documents.difference(before_documents),
            videos_add=after_videos.difference(before_videos),
        )

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

    def get_fields(self, request, obj=None):
        fields = super(CourseAdmin, self).get_fields(request, obj)
        for field in ["sold", "views", "num_of_rates", "rating"]:
            fields.remove(field)
        return fields

    def save_model(self, request, obj, form, change):
        if obj.course_of_class:
            obj.is_selling = False
        obj.save()

    def save_related(self, request, form, formsets, change):
        instance = form.instance

        before_lessons = set(instance.lessons.all())
        super().save_related(request, form, formsets, change)
        after_lessons = set(instance.lessons.all())

        lessons_remove = before_lessons.difference(after_lessons)
        lessons_add = after_lessons.difference(before_lessons)

        if lessons_remove:
            LessonManagement.objects.filter(course=instance, lesson__in=lessons_remove).delete()
            for lesson in lessons_remove:
                insert_remove_docs_videos(instance.id, lesson.id, lesson.documents.all(), lesson.videos.all(), None, None)
        if lessons_add:
            lesson_mngt_list = []
            for lesson in lessons_add:
                lesson_mngt_list.append(LessonManagement(course=instance, lesson=lesson))
                insert_remove_docs_videos(instance.id, lesson.id, None, None, lesson.documents.all(), lesson.videos.all())
            LessonManagement.objects.bulk_create(lesson_mngt_list)

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request).prefetch_related("lessons").select_related('topic')
        return qs.filter(course_of_class=False)


@admin.register(CourseManagement)
class CourseManagementAdmin(admin.ModelAdmin):
    list_filter = ("course__course_of_class", "course", "user", "sale_status")
    search_fields = (
        "user__email",
        "course__name",
        "sale_status",
    )
    list_display = (
        "user",
        "course",
        "progress",
        "mark",
        "is_done_quiz",
        "sale_status",
    )
    readonly_fields = ("progress", "user_in_class")

    def get_queryset(self, request):
        qs = super(CourseManagementAdmin, self).get_queryset(request).select_related("user", "course")
        return qs.filter(course__course_of_class=False)

    def get_fields(self, request, obj=None):
        fields = super(CourseManagementAdmin, self).get_fields(request, obj)
        for field in ["is_favorite"]:
            fields.remove(field)
        return fields


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
        return super(LessonManagementAdmin, self).get_queryset(request).select_related("lesson", "course")


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
    )

    def get_queryset(self, request):
        return super(CourseDocumentManagementAdmin, self).get_queryset(request).select_related(
            "document", "lesson", "course", "user",
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
    )

    def get_queryset(self, request):
        return super(VideoManagementAdmin, self).get_queryset(request).select_related(
            "video", "lesson", "course", "user",
        )


@admin.register(LessonQuizManagement)
class LessonQuizManagementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )

