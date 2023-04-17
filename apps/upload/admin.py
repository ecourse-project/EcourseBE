from math import ceil
import os
import json

from django.contrib import admin
from django.core.files.storage import default_storage
from django import forms

from apps.upload.models import UploadImage, UploadFile, UploadCourse, UploadDocument
from apps.upload.services.storage.base import get_file_path
from apps.upload.services.services import UploadCourseServices, UploadDocumentServices
from apps.upload.enums import video_ext_list

from moviepy.editor import VideoFileClip
from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer


@admin.register(UploadFile)
class UploadFileAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = (
        "file_name",
        "file_type",
    )
    list_display = (
        "file_name",
        "file_path",
        "file_size",
        "file_type",
        "duration",
        "created",
    )
    readonly_fields = ("file_size", "file_type", "duration", "created")

    @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    def Delete_All_Files(self, request):
        qs = self.get_queryset(request)
        if qs.exists():
            self.get_queryset(request).delete()
        return HttpResponseRedirectToReferrer(request)

    def save_model(self, request, obj, form, change):
        if not change:
            save_path, file_ext = get_file_path(file_name=obj.file_path.name, new_file_name=obj.id)
            default_storage.save(save_path, obj.file_path)
            obj.file_path = save_path
            obj.file_size = ceil(obj.file_path.size / 1024)
            obj.file_type = file_ext or None
            if file_ext and file_ext.upper() in video_ext_list:
                obj.duration = VideoFileClip(obj.file_path.path).duration

        obj.save()

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(UploadImage)
class UploadImageAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = (
        "image_name",
        "image_type",
    )
    list_display = (
        "image_name",
        "image_path",
        "image_size",
        "image_type",
        "created",
    )
    readonly_fields = ("image_size", "image_type", "created")

    @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    def Delete_All_Images(self, request):
        qs = self.get_queryset(request)
        if qs.exists():
            self.get_queryset(request).delete()
        return HttpResponseRedirectToReferrer(request)

    def save_model(self, request, obj, form, change):
        if not change:
            save_path, file_ext = get_file_path(file_name=obj.image_path.name, new_file_name=obj.id)
            default_storage.save(save_path, obj.image_path)
            obj.image_path = save_path
            obj.image_size = ceil(obj.image_path.size / 1024)
            obj.image_type = file_ext or None
        obj.save()

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class DocumentUploadForm(forms.ModelForm):
    # Define your custom form field here
    document_to_generate = forms.ChoiceField(choices=[])

    class Meta:
        model = UploadDocument
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define your custom field data retrieval logic here
        if self.instance:
            self.fields['my_custom_field'].choices = [("1", "1"), ("2", "2")]


class CourseUploadForm(forms.ModelForm):
    ROOT_DIR = "templates/data/courses/"
    course_to_generate = forms.ChoiceField(choices=[])

    class Meta:
        model = UploadCourse
        fields = '__all__'

    def get_course_title(self):
        return [name.replace("_", " ").title() for name in os.listdir(self.ROOT_DIR)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define your custom field data retrieval logic here
        if self.instance:
            self.fields["course_to_generate"].choices = [("None", "None")] + [(name, name) for name in self.get_course_title()]


@admin.register(UploadCourse)
class UploadCourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )
    form = CourseUploadForm

    def save_model(self, request, obj, form, change):
        data = None
        course_to_generate = str(form.cleaned_data.get("course_to_generate")) if str(form.cleaned_data.get("course_to_generate")) != "None" else None
        if course_to_generate:
            course_to_generate = course_to_generate.replace(" ", "_").lower()
            data = json.load(open(form.ROOT_DIR + course_to_generate + "/info.json", encoding="utf-8"))
        data = obj.data or data
        if data:
            UploadCourseServices().create_course_data([data])
        obj.save()


@admin.register(UploadDocument)
class UploadDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )
    form = DocumentUploadForm

    def save_model(self, request, obj, form, change):
        if obj.data:
            UploadDocumentServices().create_document_data(obj.data)

        obj.save()

