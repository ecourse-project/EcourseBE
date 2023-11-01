from django.contrib import admin
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from apps.posts.models import PostTopic, Post
from apps.settings.models import Header
from apps.core.general.enums import POST


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


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
    form = PostAdminForm
    readonly_fields = ("views",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "header":
            kwargs["queryset"] = Header.objects.filter(data_type=POST)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).select_related("topic")
