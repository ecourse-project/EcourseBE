from django.contrib import admin
from apps.courses.models import Course, Lesson, Topic, CourseDocument, CourseManagement
from apps.courses.enums import AVAILABLE


@admin.register(CourseDocument)
class CourseDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "title",
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
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
        "get_documents",
    )
    ordering = (
        "name",
    )

    def get_documents(self, obj):
        return ", ".join([doc.name for doc in obj.documents.all()])

    # Query objects for many to many
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "documents":
    #         kwargs["queryset"] = CourseDocument.objects.exclude(
    #             id__in=Lesson.documents.through.objects.all().values_list('coursedocument_id', flat=True)
    #         )
    #     if db_field.name == "videos":
    #         kwargs["queryset"] = UploadFile.objects.filter(file_type__iexact="mov")
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    list_display = (
        "name",
        "topic",
        "is_selling",
        "rating",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("sold", "views", "rating", "num_of_rates")

    def save_model(self, request, obj, form, change):
        if not Course.objects.filter(id=obj.id).exists():
            CourseManagement.objects.bulk_create([
                CourseManagement(course=obj, sale_status=AVAILABLE, user_id=user)
                for user in
                CourseManagement.objects.order_by('user_id').values_list('user_id', flat=True).distinct('user_id')
            ])
        obj.save()

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "lessons":
    #         kwargs["queryset"] = Lesson.objects.exclude(
    #             id__in=Course.lessons.through.objects.all().values_list('lesson_id', flat=True)
    #         )
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)





