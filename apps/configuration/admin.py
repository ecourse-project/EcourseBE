from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from apps.configuration.models import Configuration, PersonalInfo


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document_time_limit",
        "unlimited_document_time",
        "ip_address_limit",
        "unlimited_ip_addresses",
        "display_mark",
        "display_correct_answer",
    )

    list_editable = (
        "document_time_limit",
        "unlimited_document_time",
        "ip_address_limit",
        "unlimited_ip_addresses",
        "display_mark",
        "display_correct_answer",
    )

    def get_fields(self, request, obj=None):
        fields = super(ConfigurationAdmin, self).get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove("tracking_views")
        return fields

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        "id",
    )

