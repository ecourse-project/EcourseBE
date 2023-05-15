from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.configuration.api.serializers import PersonalInfoSerializer
from apps.configuration.models import PersonalInfo
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


        return render(request, "data/system/system_info.html", data)



