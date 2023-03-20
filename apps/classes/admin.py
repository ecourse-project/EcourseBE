from django.contrib import admin

from apps.classes.models import Class, ClassRequest, ClassTopic


@admin.action(description='Accept selected users')
def accept(modeladmin, request, queryset):
    queryset.update(accepted=True)
    for obj in queryset:
        obj.class_request.users.add(obj.user)


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
    list_display = (
        "name",
        "topic",
        "course",
    )


@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "class_request",
        "date_request",
        "accepted",
    )
    actions = (accept, deny)
