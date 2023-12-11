import os
import json
from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse

from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer

from apps.system.models import Storage, SystemConfig
from apps.system.services.dir_management import get_folder_size
from apps.system.choices import MEDIA, SOURCE_FE, SOURCE_BE
from apps.system.services.database_services import get_all_data


@admin.register(Storage)
class StorageAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'storage_type',
        'size_KB',
        'size_MB',
        'size_GB',
        'created',
    )

    def size_KB(self, obj):
        return round(obj.size / 1024, 2)

    def size_MB(self, obj):
        return round(obj.size / pow(1024, 2), 2)

    def size_GB(self, obj):
        return round(obj.size / pow(1024, 3), 2)

    @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    def Calculate_Media(self, request):
        if os.path.exists(settings.MEDIA_ROOT) and os.path.isdir(settings.MEDIA_ROOT):
            Storage.objects.create(storage_type=MEDIA, size=get_folder_size(settings.MEDIA_ROOT))
        return HttpResponseRedirectToReferrer(request)

    @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    def Calculate_FE(self, request):
        system_config = SystemConfig.objects.first()
        fe_path = f"{str(settings.BASE_DIR).replace(system_config.be_dir_name, '').rstrip('/')}/{system_config.fe_dir_name}"
        if os.path.exists(fe_path) and os.path.isdir(fe_path):
            Storage.objects.create(storage_type=SOURCE_FE, size=get_folder_size(fe_path))
        return HttpResponseRedirectToReferrer(request)

    @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    def Calculate_BE(self, request):
        if os.path.exists(settings.BASE_DIR) and os.path.isdir(settings.BASE_DIR):
            Storage.objects.create(storage_type=SOURCE_BE, size=get_folder_size(settings.BASE_DIR))
        return HttpResponseRedirectToReferrer(request)


@admin.register(SystemConfig)
class SystemConfigAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'fe_dir_name',
        'be_dir_name',
        'data_file_name',
    )
    list_editable = (
        'fe_dir_name',
        'be_dir_name',
        'data_file_name',
    )

    @button(change_form=True, html_attrs={'style': 'background-color:#417690;color:white'})
    def Export_data(self, request):
        data = get_all_data()
        config = SystemConfig.objects.first()
        if config and config.data_file_name:
            filename = config.data_file_name
        else:
            filename = f"exported_data_{datetime.now().date().isoformat()}.json"
        if not filename.lower().endswith(".json"):
            filename += ".json"

        response = HttpResponse(json.dumps(data), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
