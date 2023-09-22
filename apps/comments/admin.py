from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from apps.comments.models import ReplyComment, Comment


def display_content(content):
    if content:
        max_element = 10
        content_elements = content.split(" ")
        summary_content = " ".join(content_elements[:max_element])
        return summary_content + "..." if len(content_elements) > 10 else summary_content
    return ""


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "course_include",
        "class_include",
        "summary_content",
        "created",
    )

    def summary_content(self, obj):
        return display_content(obj.content)

    def name(self, obj):
        return obj.user.full_name if obj.user else ""

    def course_include(self, obj):
        if obj.course and not obj.course.course_of_class:
            return format_html(f'<a href="{settings.BASE_URL}/admin/courses/course/{obj.course.id}/change/">{obj.course.name}</a>')
        return ""

    def class_include(self, obj):
        if obj.course and obj.course.course_of_class:
            return format_html(f'<a href="{settings.BASE_URL}/admin/classes/class/{obj.course.id}/change/">{obj.course.name}</a>')
        return ""


@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "summary_content",
        "created",
    )

    def summary_content(self, obj):
        return display_content(obj.content)

    def name(self, obj):
        return obj.user.full_name if obj.user else ""
