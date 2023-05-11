from django.contrib import admin

from apps.posts.models import PostTopic, Post


@admin.register(PostTopic)
class PostTopicAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    list_display = (
        "name",
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "topic__name",
    )
    list_display = (
        "id",
        "name",
        "topic",
        "created",
    )
