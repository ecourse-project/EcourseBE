from django.contrib import admin

from apps.classes.models import Class, ClassRequest, ClassManagement
from apps.courses.services.admin import CourseAdminService, insert_remove_docs_videos
from apps.courses.models import LessonManagement


@admin.action(description='Accept selected users')
def accept(modeladmin, request, queryset):
    queryset.update(accepted=True)
    for obj in queryset:
        class_mngt = ClassManagement.objects.filter(user=obj.user, course=obj.class_request).first()
        if class_mngt:
            class_mngt.user_in_class = True
            class_mngt.save(update_fields=["user_in_class"])
        else:
            ClassManagement.objects.create(user=obj.user, course=obj.class_request, user_in_class=True)
            course_service = CourseAdminService(obj.user)
            course_service.init_courses_data([obj.class_request])


@admin.action(description='Deny selected users')
def deny(modeladmin, request, queryset):
    queryset.update(accepted=False)
    for obj in queryset:
        class_mngt = ClassManagement.objects.filter(user=obj.user, course=obj.class_request, user_in_class=True).first()
        if class_mngt:
            class_mngt.user_in_class = False
            class_mngt.save(update_fields=["user_in_class"])


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_filter = ("name", "topic")
    search_fields = (
        "name",
    )
    list_display = (
        "name",
        "topic",
        "id",
    )
    readonly_fields = ("is_selling", "price")

    def get_fields(self, request, obj=None):
        fields = super(ClassAdmin, self).get_fields(request, obj)
        for field in ["price", "is_selling", "sold", "views", "rating", "num_of_rates"]:
            fields.remove(field)
        return fields

    def save_model(self, request, obj, form, change):
        if not Class.objects.filter(id=obj.id).first():
            obj.course_of_class = True
        obj.save()

    def get_queryset(self, request):
        qs = super(ClassAdmin, self).get_queryset(request).prefetch_related("lessons").select_related('topic')
        return qs.filter(course_of_class=True)

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

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ClassAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['course'].queryset = Course.objects.filter(course_of_class=True)
    #     return form

    # def save_model(self, request, obj, form, change):
    #     obj.save()
    #     init_course_id = form.initial.get('course')
    #     if change and obj.course:
    #         if init_course_id is None or init_course_id != obj.course.id:
    #             init_course_mngt(course=obj.course, users=obj.users.all())
    #             for user in obj.users.all():
    #                 course_service = CourseAdminService(user)
    #                 course_service.init_courses_data([obj.course])


@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    list_filter = (
        "class_request__name",
        "user",
    )
    search_fields = (
        "user__email",
        "class_request__name",
    )
    list_display = (
        "user",
        "class_request",
        "date_request",
        "accepted",
    )
    actions = (accept, deny)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassRequestAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['class_request'].queryset = Class.objects.filter(course_of_class=True)
        return form

    def get_queryset(self, request):
        return super(ClassRequestAdmin, self).get_queryset(request).select_related("user", "class_request")


@admin.register(ClassManagement)
class ClassManagementAdmin(admin.ModelAdmin):
    list_filter = ("user", "course")
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
        "user_in_class",
    )
    readonly_fields = ("progress", "user_in_class", "status", "sale_status")

    def get_queryset(self, request):
        qs = super(ClassManagementAdmin, self).get_queryset(request).select_related("user", "course")
        return qs.filter(course__course_of_class=True)

    def get_fields(self, request, obj=None):
        fields = super(ClassManagementAdmin, self).get_fields(request, obj)
        for field in ["init_data", "is_favorite"]:
            fields.remove(field)
        return fields
