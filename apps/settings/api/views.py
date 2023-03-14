from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from apps.settings.services import get_headers, get_home_page, UserDataManagementService


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
        UserDataManagementService(request.user).init_user_data()
        return Response(data={"success": True})
