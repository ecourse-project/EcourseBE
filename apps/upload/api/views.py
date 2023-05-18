import os
from math import ceil

from django.conf import settings
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
from django.views import generic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from apps.upload.services.upload import upload_files, upload_images
from apps.upload.api.serializers import UploadFileSerializer, UploadImageSerializer
from apps.upload.services.storage.base import custom_get_upload_filename
from apps.upload.models import UploadImage
from ckeditor_uploader.backends import get_backend

from ckeditor_uploader.backends import get_backend
from ckeditor_uploader import utils
from ckeditor_uploader.utils import storage


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


class CustomImageUploadView(generic.View):
    http_method_names = ["post"]

    def post(self, request, **kwargs):
        uploaded_file = request.FILES["upload"]

        backend = get_backend()

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        filewrapper = backend(storage, uploaded_file)
        allow_nonimages = getattr(settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)

        if not filewrapper.is_image and not allow_nonimages:
            return HttpResponse(
                """
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '', 'Invalid file type.');
                </script>""".format(
                    ck_func_num
                )
            )

        image_id, filepath, file_ext = custom_get_upload_filename(uploaded_file.name, request)
        saved_path = filewrapper.save_as(filepath)
        url = utils.get_media_url(saved_path)

        UploadImage.objects.create(
            id=image_id,
            image_name=f"Uploaded - {uploaded_file.name}",
            image_path=filepath,
            image_size=ceil(uploaded_file.size/1024),
            image_type=file_ext,
        )

        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '{}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            _, filename = os.path.split(saved_path)
            retdata = {"url": f"{settings.BASE_URL}{url}", "uploaded": "1", "fileName": filename}
            return JsonResponse(retdata)
