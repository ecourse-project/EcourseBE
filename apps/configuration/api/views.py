from rest_framework.views import APIView
from rest_framework.response import Response

from apps.configuration.api.serializers import PersonalInfoSerializer
from apps.configuration.models import PersonalInfo


class PersonalInfoView(APIView):
    def get(self, request, *args, **kwargs):
        info = PersonalInfo.objects.all()
        if not info.exists():
            return Response(data={})
        return Response(data=PersonalInfoSerializer(info.first()).data)
