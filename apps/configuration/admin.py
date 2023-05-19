from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from apps.configuration.models import Configuration, PersonalInfo


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )


@admin.register(PersonalInfo)
class ConfigurationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        "id",
    )

