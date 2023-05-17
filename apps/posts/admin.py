from django.contrib import admin
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from apps.posts.models import PostTopic, Post
from apps.settings.models import Header
from apps.settings.enums import POST


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    header = forms.ChoiceField(choices=[])

    class Meta:
        model = Post
        fields = '__all__'

    def get_header(self):
        return Header.objects.filter(data_type=POST).values_list("display_name", flat=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define your custom field data retrieval logic here
        if self.instance:
            self.fields["header"].choices = [("None", "None")] + [(name, name) for name in self.get_header()]


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

    def save_model(self, request, obj, form, change):
        if obj.header.lower() == "none":
            obj.header = None
        obj.save()
