import json
import os.path
import shutil

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render
from django.core.serializers import serialize

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.configuration.api.serializers import PersonalInfoSerializer
from apps.configuration.models import PersonalInfo
from apps.configuration.model_choices import models
from apps.configuration.services.database_services import apply_action
from apps.core.system import get_tree_str
from apps.upload.models import UploadImage, UploadFile, UploadVideo


class PaymentInfoView(APIView):
    def get(self, request, *args, **kwargs):
        info = PersonalInfo.objects.all()
        if not info.exists():
            return Response(data={})
        return Response(data=PersonalInfoSerializer(info.first()).data)


class SystemInfoView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        file_size = round((UploadFile.objects.all().aggregate(Sum("file_size")).get("file_size__sum") or 0) / 1024, 2)
        image_size = round((UploadImage.objects.all().aggregate(Sum("image_size")).get("image_size__sum") or 0) / 1024, 2)
        video_size = round((UploadVideo.objects.all().aggregate(Sum("video_size")).get("video_size__sum") or 0) / 1024, 2)

        data = {
            "media_root": settings.MEDIA_ROOT,
            "directory": get_tree_str(settings.MEDIA_ROOT),
            "storage": {
                "file": file_size,
                "image": image_size,
                "video": video_size,
                "total": file_size + image_size + video_size,
            }
        }

        return render(request, "data/system/system_info.html", data)


class GetDataFromDatabase(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        query_params = self.request.query_params
        model = models.get(query_params.get("model", "").strip())
        data = json.loads(query_params.get("data", "{}").strip())
        action = query_params.get("action", "").strip().lower()
        extra_action = query_params.get("extra_action", "").strip().lower()

        response_data_string = "No data"
        if model:
            output_data = apply_action(model=model, data=data, action=action, extra_action=extra_action)
            if isinstance(output_data, int) or isinstance(output_data, str):
                response_data_string = output_data
            else:
                response_data_json = serialize(
                    'json',
                    [output_data] if isinstance(output_data, model) else output_data,
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True
                )
                response_data_string = json.dumps(json.loads(response_data_json), indent=4)

        context = {
            "response_data_string": response_data_string,
        }

        return render(request, "data/system/database_display.html", context)


class DirectoryManagement(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        delete_path = self.request.query_params.get("path", "").strip()
        full_path = os.path.join(settings.MEDIA_ROOT, delete_path).replace("/", "\\")
        message = f"{full_path} deleted"

        try:
            if os.path.isdir(full_path):
                os.rmdir(full_path)
            else:
                os.remove(full_path)
        except Exception:
            message = f"Cannot delete {full_path}"

        context = {
            "message": message,
        }
        return render(request, "data/system/directory_management.html", context)



