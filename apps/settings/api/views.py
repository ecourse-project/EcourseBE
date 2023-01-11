from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.settings.models import HeaderDetail, Header


class HeaderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        header_dict = {}
        for header in Header.objects.all():
            header_dict[header.display_name] = [detail.display_name for detail in header.header_detail.all()]
        return Response(header_dict)
