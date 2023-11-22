from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect

from apps.users.models import User
from apps.classes.models import Class, ClassRequest, ClassManagement
from apps.classes.services.admin import join_class_single_request, AdminClassPermissons
from apps.classes.services.admin_action import accept, deny
from apps.courses.models import (
    Lesson,
    LessonManagement,
    CourseDocumentManagement,
    VideoManagement,
    CourseTopic,
)
from apps.courses.forms import CourseForm
from apps.core.general.init_data import UserDataManagementService
from apps.core.general.admin_site import get_admin_attrs


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "Class", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "Class", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "Class", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "Class", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "Class", "list_display")

    form = CourseForm
    filter_horizontal = ("lessons",)
    change_form_template = "admin_button/remove_lesson.html"

    def response_change(self, request, obj):
        if "remove-lesson" in request.POST:
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassAdmin, self).get_form(request, obj, **kwargs)
        filter_condition = AdminClassPermissons(request.user).user_condition()
        form.base_fields['topic'].queryset = CourseTopic.objects.filter(filter_condition)
        form.base_fields['lessons_remove'].queryset = Lesson.objects.filter(filter_condition & Q(removed=False))
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        filter_condition = AdminClassPermissons(request.user).user_condition()
        filter_condition &= Q(removed=False)
        if db_field.name == "lessons":
            kwargs["queryset"] = Lesson.objects.filter(filter_condition)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        filter_condition = AdminClassPermissons(request.user).get_filter_condition()
        return (
            super(ClassAdmin, self)
            .get_queryset(request)
            .prefetch_related("lessons")
            .select_related('topic', 'author')
            .filter(filter_condition)
        )

    def save_model(self, request, obj, form, change):
        if not Class.objects.filter(id=obj.id).exists():
            obj.course_of_class = True
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


@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    actions = (accept, deny)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "ClassRequest", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "ClassRequest", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "ClassRequest", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "ClassRequest", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "ClassRequest", "list_display")

    def name(self, obj):
        return obj.user.full_name if obj.user else ""

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassRequestAdmin, self).get_form(request, obj, **kwargs)
        filter_condition = AdminClassPermissons(request.user).get_filter_condition()
        form.base_fields['class_request'].queryset = Class.objects.filter(filter_condition)
        return form

    def get_queryset(self, request):
        filter_condition = AdminClassPermissons(request.user).get_filter_condition("class_request")
        return (
            super(ClassRequestAdmin, self)
            .get_queryset(request)
            .select_related("user", "class_request")
            .filter(filter_condition)
        )

    def save_model(self, request, obj, form, change):
        obj.save()
        join_class_single_request(obj)

    def delete_model(self, request, obj):
        class_mngt = ClassManagement.objects.filter(user=obj.user, course=obj.class_request).first()
        if class_mngt:
            class_mngt.user_in_class = False
            class_mngt.save(update_fields=["user_in_class"])
        obj.delete()

    def delete_queryset(self, request, queryset):
        qs = Q()
        for obj in queryset:
            qs |= Q(user=obj.user, course=obj.class_request) if obj.user and obj.class_request and obj.accepted else Q()
        ClassManagement.objects.filter(qs).update(user_in_class=False)
        queryset.delete()


@admin.register(ClassManagement)
class ClassManagementAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "ClassManagement", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "ClassManagement", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "ClassManagement", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "ClassManagement", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "ClassManagement", "list_display")

    def get_queryset(self, request):
        filter_condition = AdminClassPermissons(request.user).get_filter_condition("course")
        return (
            super(ClassManagementAdmin, self)
            .get_queryset(request)
            .select_related("user", "course")
            .filter(filter_condition)
            .order_by("course")
        )

    def has_delete_permission(self, request, obj=None):
        if obj and ClassRequest.objects.filter(user=obj.user, class_request=obj.course, accepted=True):
            return False
        # if ClassRequest.objects.filter(user=obj.user, class_request=obj.course, accepted=True)
        return True

    def has_add_permission(self, request):
        return get_admin_attrs(request, "ClassManagement", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "ClassManagement", "has_change_permission")


