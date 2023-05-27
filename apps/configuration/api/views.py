from rest_framework.views import APIView
from rest_framework.response import Response

from apps.configuration.api.serializers import PersonalInfoSerializer
from apps.configuration.models import PersonalInfo
from apps.core.general.services import search_item


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
