import os

from django.contrib import admin
from django.conf import settings
from django.db.models import Q
from django.utils.html import format_html

from apps.core.utils import get_default_hidden_file_type
from apps.upload.models import (
    UploadImage,
    UploadFile,
    UploadVideo,
    UploadAvatar,
    UploadFolder,
)
from apps.upload.services.storage.base import (
    store_file_upload,
    upload_and_unzip_folder,
)
from apps.upload.enums import VIDEO, IMAGE, FILE
from apps.upload.forms import UploadFolderForm

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
        "order",
        "created",
    )
    readonly_fields = ("video_size", "video_type", "duration", "created")
    # actions = (delete_data,)

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

    def get_fields(self, request, obj=None):
        fields = super(UploadVideoAdmin, self).get_fields(request, obj)
        fields.remove("ip_address")
        return fields

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
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
    # actions = (delete_data,)

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

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()

    def get_fields(self, request, obj=None):
        fields = super(UploadFileAdmin, self).get_fields(request, obj)
        fields.remove("ip_address")
        return fields

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

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
    # actions = (delete_data,)

    def image_url(self, obj):
        url = settings.BASE_URL + obj.image_path.url
        return format_html(f'<a href="{url}">{url}</a>')

    def get_queryset(self, request):
        return super(UploadImageAdmin, self).get_queryset(request).filter(is_avatar=False)

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()
    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Images(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def get_fields(self, request, obj=None):
        fields = super(UploadImageAdmin, self).get_fields(request, obj)
        fields.remove("ip_address")
        return fields

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


@admin.register(UploadAvatar)
class UploadAvatarAdmin(admin.ModelAdmin):
    search_fields = (
        "image_name",
    )
    list_display = (
        "image_name",
        "image_url",
        "image_size",
        "image_type",
        "created",
    )
    readonly_fields = ("image_size", "image_type", "created")

    def image_url(self, obj):
        url = settings.BASE_URL + obj.image_path.url
        return format_html(f'<a href="{url}">{url}</a>')

    def get_queryset(self, request):
        return super(UploadAvatarAdmin, self).get_queryset(request).filter(is_avatar=True)

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()

    def get_fields(self, request, obj=None):
        fields = super(UploadAvatarAdmin, self).get_fields(request, obj)
        fields.remove("ip_address")
        return fields


@admin.register(UploadFolder)
class UploadFolderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created",
    )
    form = UploadFolderForm

    def save_model(self, request, obj, form, change):
        obj.folder_path = None
        obj.save()
