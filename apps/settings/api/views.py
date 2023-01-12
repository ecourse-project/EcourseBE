from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.settings.models import Header
from apps.settings.services import get_obj_type


class HeaderAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        header_dict = {}
        for header in Header.objects.all():
            header_dict[header.display_name] = {}
            header_detail = header.header_detail.all().order_by("display_name")
            if header_detail.exists():
                header_dict[header.display_name] = {
                    "type": get_obj_type(header_detail.first()),
                    "title": [detail.display_name for detail in header_detail]
                }
        return Response(header_dict)
