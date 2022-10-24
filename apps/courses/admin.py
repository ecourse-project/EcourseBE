from django.contrib import admin
from django.db.models import Q
from apps.courses.models import (
    Course,
    Lesson,
    Topic,
    CourseDocument,
    LessonManagement,
    CourseDocumentManagement,
    VideoManagement,
)
from apps.courses.enums import BOUGHT
from apps.courses.services.admin import (
    init_course_mngt,
    update_course_doc_mngt,
    update_video_mngt,
    get_users_by_course_sale_status,
    add_docs_to_lesson,
    add_videos_to_lesson,
)
from apps.upload.models import UploadFile
from apps.upload.enums import video_ext_list
from apps.users.services import get_active_users
from apps.users.models import User
from apps.courses.services.services import CourseManagementService
from apps.rating.models import CourseRating


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
        instance = form.instance

        before_documents = set(instance.documents.all())
        before_videos = set(instance.videos.all())
        super().save_related(request, form, formsets, change)
        after_documents = set(instance.documents.all())
        after_videos = set(instance.videos.all())

        courses_include_lesson = (
            LessonManagement.objects.filter(lesson=instance, is_available=True)
            .distinct("course_id")
            .values_list("course_id", flat=True)
        )

        update_course_doc_mngt(
            docs_remove=before_documents.difference(after_documents),
            docs_add=after_documents.difference(before_documents),
            lesson=instance,
            courses_include_lesson=courses_include_lesson,
        )
        update_video_mngt(
            videos_remove=before_videos.difference(after_videos),
            videos_add=after_videos.difference(before_videos),
            lesson=instance,
            courses_include_lesson=courses_include_lesson,
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
        if not Course.objects.filter(id=obj.id).first():
            """ Init course data """
            users = get_active_users()
            if users.count() > 0:
                init_course_mngt(obj, users)
        obj.save()

        """ Init course rating """
        rating, _ = CourseRating.objects.get_or_create(course=obj)

    def save_related(self, request, form, formsets, change):
        instance = form.instance

        before_lessons = set(instance.lessons.all())
        super().save_related(request, form, formsets, change)
        after_lessons = set(instance.lessons.all())

        users_id = get_users_by_course_sale_status(course_id=instance.id, sale_status=BOUGHT)
        if users_id and (before_lessons or after_lessons):
            lessons_remove = before_lessons.difference(after_lessons)
            lessons_add = after_lessons.difference(before_lessons)

            if lessons_remove:
                LessonManagement.objects.filter(course=instance, lesson__in=lessons_remove).update(is_available=False)
                CourseDocumentManagement.objects.filter(course=instance, lesson__in=lessons_remove).update(is_available=False)
                VideoManagement.objects.filter(course=instance, lesson__in=lessons_remove).update(is_available=False)
                for user_id in users_id:
                    CourseManagementService(User.objects.get(id=user_id)).calculate_course_progress(course_id=instance.id)

            if lessons_add:
                list_lesson_objs = []
                for user_id in users_id:
                    for lesson in lessons_add:
                        lesson_obj, _ = LessonManagement.objects.get_or_create(course=instance, lesson=lesson, user_id=user_id)
                        if lesson_obj:
                            lesson_obj.is_available = True
                            list_lesson_objs.append(lesson_obj)
                LessonManagement.objects.bulk_update(list_lesson_objs, ["is_available"])

                for lesson in lessons_add:
                    add_docs_to_lesson(lesson.documents.all(), lesson, [instance.id])
                    add_videos_to_lesson(lesson.videos.all(), lesson, [instance.id])
