from django.contrib import admin
from django.db.models import Q
from apps.courses.models import Course, Lesson, Topic, CourseDocument, CourseManagement
from apps.courses.enums import AVAILABLE
from apps.courses.signals import calculate_progress
from apps.upload.models import UploadFile
from apps.upload.enums import video_ext_list


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
        "list_documents",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("total_documents", "total_videos")

    def list_documents(self, obj):
        return ", ".join([doc.name for doc in obj.documents.all()])

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.total_documents = instance.documents.all().count()
        instance.total_videos = instance.videos.all().count()
        instance.save(update_fields=["total_documents", "total_videos"])

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
        "name",
    )
    list_display = (
        "name",
        "topic",
        "total_lessons",
        "is_selling",
        "rating",
    )
    ordering = (
        "name",
    )
    readonly_fields = ("sold", "views", "rating", "num_of_rates", "total_lessons")

    def save_model(self, request, obj, form, change):
        # if create a course, it means obj is not exist in database
        if not Course.objects.filter(id=obj.id).exists():
            CourseManagement.objects.bulk_create([
                CourseManagement(course=obj, sale_status=AVAILABLE, user_id=user)
                for user in
                CourseManagement.objects.order_by('user_id').values_list('user_id', flat=True).distinct('user_id')
            ])
        obj.save()

    def save_related(self, request, form, formsets, change):
        before_lesson = set(form.instance.lessons.all())
        super().save_related(request, form, formsets, change)
        after_lesson = set(form.instance.lessons.all())

        instance = form.instance
        instance.total_lessons = instance.lessons.all().count()
        instance.save(update_fields=['total_lessons'])

        # remove lesson from course
        if len(after_lesson) < len(before_lesson):
            diff_lesson = before_lesson ^ after_lesson
            for lesson in diff_lesson:
                for course_mngt in CourseManagement.objects.filter(course=instance):
                    course_mngt.docs_completed.remove(*lesson.documents.all())
                    course_mngt.videos_completed.remove(*lesson.videos.all())

        # add lesson to course
        elif len(after_lesson) > len(before_lesson):
            for course_mngt in CourseManagement.objects.filter(course=instance):
                calculate_progress(course_mngt)


    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "lessons":
    #         kwargs["queryset"] = Lesson.objects.exclude(
    #             id__in=Course.lessons.through.objects.all().values_list('lesson_id', flat=True)
    #         )
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)





