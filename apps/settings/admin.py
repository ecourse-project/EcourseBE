from django.contrib import admin

from apps.settings.models import Header, HeaderDetail


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_name",
    )


@admin.register(HeaderDetail)
class HeaderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "header",
        "document_title",
        "course_title",
    )
