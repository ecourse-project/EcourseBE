from django.contrib import admin
from django.db.models import Q
from apps.courses.models import (
    Course,
    Lesson,
    CourseTopic,
    CourseDocument,
    LessonManagement,
    CourseManagement,
)
from apps.courses.services.admin import (
    insert_remove_docs_videos,
)
from apps.courses.enums import AVAILABLE, IN_CART
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

    def get_form(self, request, obj=None, **kwargs):
        form = super(CourseDocumentAdmin, self).get_form(request, obj, **kwargs)
        q_list = Q()
        for q in [Q(file_type__iexact=ext) for ext in video_ext_list]:
            q_list |= q
        form.base_fields['file'].queryset = UploadFile.objects.filter(~q_list)
        return form


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
        "list_documents",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("total_documents", "total_videos")

    def list_documents(self, obj):
        return ", ".join([doc.name for doc in obj.documents.all()])

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
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # if db_field.name == "documents":
        #     kwargs["queryset"] = CourseDocument.objects.exclude(
        #         id__in=Lesson.documents.through.objects.all().values_list('coursedocument_id', flat=True)
        #     )

        if db_field.name == "videos":
            q_list = Q()
            for q in [Q(file_type__iexact=ext) for ext in video_ext_list]:
                q_list |= q
            kwargs["queryset"] = UploadFile.objects.filter(q_list)
            # kwargs["queryset"] = UploadFile.objects.filter(file_type__iexact="mov")
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "name",
    )
    list_display = (
        "id",
        "name",
        "topic",
        "total_lessons",
        "price",
        "is_selling",
        "rating",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("sold", "views", "rating", "num_of_rates", "total_lessons")

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

    # def delete_model(self, request, obj):
    #     CourseManagement.objects.filter(course=obj, sale_status__in=[AVAILABLE, IN_CART]).delete()
    #     obj.delete()


@admin.register(CourseManagement)
class CourseManagementAdmin(admin.ModelAdmin):
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




