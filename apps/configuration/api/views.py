import json
import os.path
# import subprocess

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
from apps.configuration.services.dir_management import apply_dir_action
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

        context = {
            "base_dir": settings.BASE_DIR,
            "media_root": settings.MEDIA_ROOT,
            "directory": get_tree_str(settings.BASE_DIR / "apps"),
            "media": get_tree_str(settings.MEDIA_ROOT),
            "storage": {
                "file": file_size,
                "image": image_size,
                "video": video_size,
                "total": file_size + image_size + video_size,
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
        action = self.request.query_params.get("action", "").strip()
        root = self.request.query_params.get("root", settings.MEDIA_ROOT).strip()
        source = self.request.query_params.get("source", "").strip()
        destination = self.request.query_params.get("destination", "").strip()
        file_type = self.request.query_params.get("file_type", "").strip()

        if root == "base":
            root = settings.BASE_DIR
        else:
            root = settings.MEDIA_ROOT
        root = root.replace(chr(92), "/").strip("/")

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
        # # Command to execute
        # command = "pg_dump -U postgres ecourse-release > D:\diephaibinh.sql"
        #
        # # Execute the command
        # result = subprocess.run(command, shell=True, capture_output=True, text=True)
        #
        # # Check the result
        # if result.returncode == 0:
        #     # Command executed successfully
        #     output = result.stdout
        #     print(output)
        # else:
        #     # An error occurred
        #     error = result.stderr
        #     print(f"Command execution failed: {error}")

        return Response()


