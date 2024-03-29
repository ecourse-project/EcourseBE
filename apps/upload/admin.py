import os

from django.contrib import admin
from django.conf import settings
from django.db.models import Q
from django.utils.html import format_html

from admin_extra_buttons.api import ExtraButtonsMixin, button
from ipware.ip import get_client_ip

from apps.core.general.admin_site import get_admin_attrs
from apps.core.utils import get_default_hidden_file_type, delete_directory
from apps.upload.models import (
    UploadImage,
    UploadFile,
    UploadVideo,
    UploadAvatar,
    UploadFolder,
)
from apps.upload.services.storage.base import (
    store_file_upload,
)
from apps.upload.enums import VIDEO, IMAGE, FILE
from apps.upload.forms import UploadFolderForm
from apps.upload.services.services import find_dir_by_instance
from apps.upload.services.admin import AdminUploadPermissons


@admin.action(description='Delete records and files for selected data')
def delete_data(modeladmin, request, queryset):
    for data in queryset:
        data.delete()


@admin.register(UploadVideo)
class UploadVideoAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    # actions = (delete_data,)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadVideo", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadVideo", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "UploadVideo", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "UploadVideo", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "UploadVideo", "list_display")


    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Videos(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def save_model(self, request, obj, form, change):
        if not UploadVideo.objects.filter(id=obj.id).exists():
            obj.author = request.user

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

    def get_queryset(self, request):
        filter_condition = AdminUploadPermissons(request.user).user_condition()
        return (
            super(UploadVideoAdmin, self)
            .get_queryset(request)
            .select_related('author')
            .filter(filter_condition)
        )

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    # actions = (delete_data,)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadFile", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadFile", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "UploadFile", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "UploadFile", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "UploadFile", "list_display")

    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Files(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def get_queryset(self, request):
        filter_condition = AdminUploadPermissons(request.user).user_condition()
        return (
            super(UploadFileAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(
                ~Q(file_type__in=get_default_hidden_file_type())
                & filter_condition
            )
        )

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()

    # def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
    #     context.update({
    #         'show_save_and_continue': False,
    #     })
    #     return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        if not UploadFile.objects.filter(id=obj.id).exists():
            obj.author = request.user

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
    # actions = (delete_data,)

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadImage", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadImage", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "UploadImage", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "UploadImage", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "UploadImage", "list_display")

    def image_url(self, obj):
        url = settings.BASE_URL + obj.image_path.url
        return format_html(f'<a href="{url}">{url}</a>')

    def get_queryset(self, request):
        filter_condition = AdminUploadPermissons(request.user).user_condition()
        return (
            super(UploadImageAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(Q(is_avatar=False) & filter_condition)
        )

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()

    # @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    # def Delete_All_Images(self, request):
    #     qs = self.get_queryset(request)
    #     if qs.exists():
    #         self.get_queryset(request).delete()
    #     return HttpResponseRedirectToReferrer(request)

    def save_model(self, request, obj, form, change):
        if not UploadImage.objects.filter(id=obj.id).exists():
            obj.author = request.user

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
    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadAvatar", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadAvatar", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "UploadAvatar", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "UploadAvatar", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "UploadAvatar", "list_display")

    def image_url(self, obj):
        url = settings.BASE_URL + obj.image_path.url
        return format_html(f'<a href="{url}">{url}</a>')

    def get_queryset(self, request):
        return (
            super(UploadAvatarAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(is_avatar=True)
        )

    def delete_queryset(self, request, queryset):
        for data in queryset:
            data.delete()

    def has_add_permission(self, request):
        return get_admin_attrs(request, "UploadAvatar", "has_add_permission")

    def has_change_permission(self, request, obj=None):
        return get_admin_attrs(request, "UploadAvatar", "has_change_permission")

    def has_delete_permission(self, request, obj=None):
        return get_admin_attrs(request, "UploadAvatar", "has_delete_permission")


@admin.register(UploadFolder)
class UploadFolderAdmin(admin.ModelAdmin):
    form = UploadFolderForm

    def get_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadFolder", "fields")

    def get_readonly_fields(self, request, obj=None):
        return get_admin_attrs(request, "UploadFolder", "readonly_fields")

    def get_list_filter(self, request):
        return get_admin_attrs(request, "UploadFolder", "list_filter")

    def get_search_fields(self, request):
        return get_admin_attrs(request, "UploadFolder", "search_fields")

    def get_list_display(self, request):
        return get_admin_attrs(request, "UploadFolder", "list_display")

    def save_model(self, request, obj, form, change):
        if not UploadFolder.objects.filter(id=obj.id).exists():
            obj.author = request.user
        obj.folder_path = None
        obj.save()

    def get_queryset(self, request):
        filter_condition = AdminUploadPermissons(request.user).user_condition()
        return (
            super(UploadFolderAdmin, self)
            .get_queryset(request)
            .select_related("author")
            .filter(filter_condition)
        )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            delete_directory(find_dir_by_instance(obj))
        queryset.delete()

    def delete_model(self, request, obj):
        directory_path = find_dir_by_instance(obj)
        delete_directory(directory_path)
        obj.delete()
