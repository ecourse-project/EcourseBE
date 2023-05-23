import os
import json

from django.contrib import admin
from django import forms
from django.conf import settings
from django.db.models import Q

from apps.core.utils import get_default_hidden_file_type
from apps.upload.models import UploadImage, UploadFile, UploadVideo, UploadCourse, UploadDocument
from apps.upload.services.storage.base import store_file_upload
from apps.upload.services.services import UploadCourseServices, UploadDocumentServices
from apps.upload.enums import VIDEO, IMAGE, FILE

from admin_extra_buttons.api import ExtraButtonsMixin, button
from ipware.ip import get_client_ip


@admin.action(description='Delete records and files for selected data')
def delete_data(modeladmin, request, queryset):
    for data in queryset:
        data.delete()


@admin.register(UploadVideo)
class UploadVideoAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = (
        "video_name",
        "video_type",
    )
    list_display = (
        "video_name",
        "video_path",
        "video_size",
        "video_type",
        "duration",
        "created",
    )
    readonly_fields = ("video_size", "video_type", "duration", "created")
    actions = (delete_data,)

    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Videos(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def save_model(self, request, obj, form, change):
        if change:
            if obj.video_path and str(form.initial.get("video_path")) != str(obj.video_path):
                if form.initial.get("video_path"):
                    try:
                        os.remove(form.initial.get("video_path").path)
                    except Exception:
                        pass
                store_file_upload(obj, obj.video_path, VIDEO)
        else:
            if obj.video_path:
                store_file_upload(obj, obj.video_path, VIDEO)
        obj.ip_address = get_client_ip(request)
        obj.save()


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
        "created",
    )
    readonly_fields = ("file_size", "file_type", "created")
    actions = (delete_data,)

    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Files(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def get_queryset(self, request):
        return super(UploadFileAdmin, self).get_queryset(request).filter(
            ~Q(file_type__in=get_default_hidden_file_type())
        )

    def save_model(self, request, obj, form, change):
        if change:
            if obj.file_path and str(form.initial.get("file_path")) != str(obj.file_path):
                if form.initial.get("file_path"):
                    try:
                        os.remove(form.initial.get("file_path").path)
                    except Exception:
                        pass
                store_file_upload(obj, obj.file_path, FILE)
        else:
            if obj.file_path:
                store_file_upload(obj, obj.file_path, FILE)

        obj.ip_address = get_client_ip(request)
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
        "image_url",
        "image_size",
        "image_type",
        "created",
    )
    readonly_fields = ("image_size", "image_type", "created")
    actions = (delete_data,)

    def image_url(self, obj):
        return settings.BASE_URL + obj.image_path.url

    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Images(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def save_model(self, request, obj, form, change):
        if change:
            if obj.image_path and str(form.initial.get("image_path")) != str(obj.image_path):
                if form.initial.get("image_path"):
                    try:
                        os.remove(form.initial.get("image_path").path)
                    except Exception:
                        pass
                store_file_upload(obj, obj.image_path, IMAGE)
        else:
            if obj.image_path:
                store_file_upload(obj, obj.image_path, IMAGE)

        obj.ip_address = get_client_ip(request)
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
            self.fields["document_to_generate"].choices = [("1", "1"), ("2", "2")]


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
        "name",
        "is_class",
    )
    form = CourseUploadForm

    def save_model(self, request, obj, form, change):
        if not change:
            data = obj.data
            if not data:
                course_to_generate = str(form.cleaned_data.get("course_to_generate")) if str(form.cleaned_data.get("course_to_generate")) != "None" else None
                if course_to_generate:
                    course_to_generate = course_to_generate.replace(" ", "_").lower()
                    data = json.load(open(form.ROOT_DIR + course_to_generate + "/info.json", encoding="utf-8"))
                    data["course_of_class"] = obj.is_class
            if data:
                obj.name = data.get("name")
                UploadCourseServices().create_course_data([data])

        obj.save()


@admin.register(UploadDocument)
class UploadDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    form = DocumentUploadForm

    def save_model(self, request, obj, form, change):
        if obj.data and not change:
            obj.name = obj.data.get("name")
            UploadDocumentServices().create_document_data(obj.data)

        obj.save()



