from django.contrib import admin

from apps.settings.models import Header, HeaderDetail, HomePageDetail
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "data_type",
        "order",
    )


@admin.register(HeaderDetail)
class HeaderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "header",
        "order",
        "document_topic",
        "course_and_class_topic",
        "post_topic",
    )


@admin.register(HomePageDetail)
class HomePageDetailAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        "display_name",
        "created",
    )
