from django.contrib import admin

from apps.classes.models import Class, ClassRequest, ClassManagement
from apps.courses.services.admin import CourseAdminService


@admin.action(description='Accept selected users')
def accept(modeladmin, request, queryset):
    queryset.update(accepted=True)
    for obj in queryset:
        _, created = ClassManagement.objects.get_or_create(user=obj.user, course=obj.class_request, user_in_class=True)
        if created:
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
    search_fields = (
        "name",
    )
    list_display = (
        "id",
        "name",
        "topic",
    )
    readonly_fields = ("course_of_class", "is_selling", "sold", "views", "num_of_rates", "rating")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(course_of_class=True)

    def save_model(self, request, obj, form, change):
        obj.course_of_class = True
        obj.save()

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

    def save_model(self, request, obj, form, change):
        # if not ClassRequest.objects.filter(user=obj.user, class_request=obj.class_request).exists():
        #     print(111111111111111111111111111111111)
        obj.save()


@admin.register(ClassManagement)
class ClassManagementAdmin(admin.ModelAdmin):
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
    readonly_fields = ("progress", "user_in_class")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(course__course_of_class=True)
