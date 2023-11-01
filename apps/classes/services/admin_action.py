from django.contrib import admin

from apps.classes.services.admin import join_class_multiple_requests


@admin.action(description='Accept selected users')
def accept(modeladmin, request, queryset):
    queryset.update(accepted=True)
    join_class_multiple_requests(queryset, True)


@admin.action(description='Deny selected users')
def deny(modeladmin, request, queryset):
    queryset.update(accepted=False)
    join_class_multiple_requests(queryset, False)
