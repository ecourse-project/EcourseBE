from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from apps.configuration.models import Configuration, PersonalInfo


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document_time_limit",
        "document_unlimited_time",
    )

    list_editable = (
        "document_time_limit",
        "document_unlimited_time",
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        "id",
    )

