from django.contrib import admin

from apps.classes.models import Class, ClassRequest, ClassTopic
from apps.courses.services.admin import CourseAdminService, init_course_mngt
from apps.courses.models import CourseManagement, Course


@admin.action(description='Accept selected users')
def accept(modeladmin, request, queryset):
    queryset.update(accepted=True)
    list_course_mngt = []
    for obj in queryset:
        obj.class_request.users.add(obj.user)
        course = obj.class_request.course
        if course:
            list_course_mngt.append(CourseManagement(user=obj.user, course=course))
            course_service = CourseAdminService(obj.user)
            course_service.init_courses_data([course])
    CourseManagement.objects.bulk_create(list_course_mngt)


@admin.action(description='Deny selected users')
def deny(modeladmin, request, queryset):
    queryset.update(accepted=False)
    for obj in queryset:
        obj.class_request.users.remove(obj.user)


@admin.register(ClassTopic)
class ClassTopicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "course__name",
    )
    list_display = (
        "id",
        "name",
        "topic",
        "course",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['course'].queryset = Course.objects.filter(course_of_class=True)
        return form

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
