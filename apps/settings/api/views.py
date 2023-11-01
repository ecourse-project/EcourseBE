from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.configuration.models import Configuration
from apps.users.services import tracking_user_device
from apps.settings.services import get_headers, get_home_page
from apps.core.general.init_data import UserDataManagementService


class HeaderAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(get_headers())


class HomePageAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(get_home_page())


class InitData(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if Configuration.objects.first():
            tracking_user_device(request)
        if user and not user.is_anonymous and user.is_authenticated and not user.first_login:
            UserDataManagementService(user).create_multiple_course_mngt_for_user()

        return Response(data={"success": True})
