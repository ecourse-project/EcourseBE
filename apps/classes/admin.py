from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect

from apps.classes.models import Class, ClassRequest, ClassManagement
from apps.classes.services.admin import join_class_single_request
from apps.classes.services.admin_action import accept, deny
from apps.courses.models import LessonManagement, CourseDocumentManagement, VideoManagement
from apps.courses.forms import CourseForm
from apps.core.general.init_data import UserDataManagementService


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
    filter_horizontal = ("lessons",)
    form = CourseForm
    change_form_template = "admin_button/remove_lesson.html"

    def response_change(self, request, obj):
        if "remove-lesson" in request.POST:
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def get_fields(self, request, obj=None):
        fields = super(ClassAdmin, self).get_fields(request, obj)
        for field in ["price", "is_selling"]:
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
    list_filter = (
        "class_request__name",
    )
    search_fields = (
        "user__email",
        "user__full_name",
        "class_request__name",
    )
    list_display = (
        "user",
        "name",
        "class_request",
        "date_request",
        "accepted",
    )
    actions = (accept, deny)

    def name(self, obj):
        return obj.user.full_name if obj.user else ""

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassRequestAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['class_request'].queryset = Class.objects.filter(course_of_class=True)
        return form

    def get_queryset(self, request):
        return super(ClassRequestAdmin, self).get_queryset(request).select_related("user", "class_request")

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
    list_filter = ("course", "user_in_class")
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
    readonly_fields = ("progress", "status", "sale_status", "views")

    def get_queryset(self, request):
        qs = super(ClassManagementAdmin, self).get_queryset(request).select_related("user", "course")
        return qs.filter(course__course_of_class=True)

    def get_fields(self, request, obj=None):
        fields = super(ClassManagementAdmin, self).get_fields(request, obj)
        remove_fields = ["is_favorite", "sale_status"]
        if not request.user.is_superuser:
            remove_fields.extend(["views"])
        for field in remove_fields:
            fields.remove(field)
        return fields

    def get_list_display(self, request):
        list_display = super(ClassManagementAdmin, self).get_list_display(request)
        if request.user.is_superuser:
            list_display = tuple(list(list_display) + ["views"])
            return list_display
        return list_display

    def has_delete_permission(self, request, obj=None):
        if obj and ClassRequest.objects.filter(user=obj.user, class_request=obj.course, accepted=True):
            return False
        # if ClassRequest.objects.filter(user=obj.user, class_request=obj.course, accepted=True)
        return True


