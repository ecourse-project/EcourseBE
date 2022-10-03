from rest_framework.views import APIView
from apps.upload.services.upload import upload_files, upload_images
from rest_framework.response import Response
from rest_framework import generics, status
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer


class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        upload_file = upload_files(request=self.request)
        data = UploadFileSerializer(upload_file, many=True).data
        return Response(data=data, status=status.HTTP_201_CREATED)


class UploadImageView(APIView):
    def post(self, request, *args, **kwargs):
        upload_file = upload_images(request=self.request)
        data = UploadImageSerializer(upload_file, many=True).data
        return Response(data=data, status=status.HTTP_201_CREATED)
