from django.contrib import admin
from django.core.files.storage import default_storage

from apps.upload.models import UploadImage, UploadFile
from apps.upload.services.storage.base import get_file_path
from apps.upload.enums import video_ext_list
from moviepy.editor import VideoFileClip


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "file_path",
        "file_size",
        "file_type",
        "created",
    )
    readonly_fields = ("file_size", "file_type", "duration")

    def save_model(self, request, obj, form, change):
        if not change:
            save_path = get_file_path(file_name=obj.file_path.name)
            default_storage.save(save_path, obj.file_path)
            obj.file_path = save_path
            obj.file_size = obj.file_path.size
            obj.file_type = obj.file_path.name.split(".")[-1]
            print(obj.file_type.upper())
            if obj.file_type.upper() in video_ext_list:
                obj.duration = VideoFileClip(obj.file_path.path).duration

        obj.save()

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UploadImage)
class UploadImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_path",
        "image_size",
        "image_type",
        "created",
    )
    readonly_fields = ("image_size", "image_type")

    def save_model(self, request, obj, form, change):
        if not change:
            save_path = get_file_path(file_name=obj.image_path.name)
            default_storage.save(save_path, obj.image_path)
            obj.image_path = save_path
            obj.image_size = obj.image_path.size
            obj.image_type = obj.image_path.name.split(".")[-1]
        obj.save()

    def has_change_permission(self, request, obj=None):
        return False
