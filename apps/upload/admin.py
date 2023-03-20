from math import ceil

from django.contrib import admin
from django.core.files.storage import default_storage

from apps.upload.models import UploadImage, UploadFile
from apps.upload.services.storage.base import get_file_path
from apps.upload.enums import video_ext_list

from moviepy.editor import VideoFileClip
from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer


@admin.register(UploadFile)
class UploadFileAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = (
        "file_name",
        "file_path",
        "file_size",
        "file_type",
        "duration",
        "created",
    )
    readonly_fields = ("file_path", "file_size", "file_type", "duration", "created")

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
    list_display = (
        "image_name",
        "image_path",
        "image_size",
        "image_type",
        "created",
    )
    readonly_fields = ("image_path", "image_size", "image_type", "created")

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

