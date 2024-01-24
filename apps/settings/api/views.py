from django.db.models import F

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.system.models import VisitStatistics
from apps.configuration.models import Configuration
from apps.users.services import tracking_user_device
from apps.settings.services import get_headers, get_home
from apps.core.general.init_data import UserDataManagementService
from apps.core.general.services import response_search_item
from apps.core.general.enums import ALL
from apps.core.utils import get_now


class HeaderAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(get_headers())


class HomePageAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        now = get_now()
        visit_statistic = VisitStatistics.objects.filter(created__date=now.date()).first()
        if not visit_statistic:
            visit_statistic = VisitStatistics.objects.create()
        visit_statistic.visit = F("visit") + 1
        visit_statistic.save(update_fields=["visit"])

        return Response(get_home())


class InitData(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if Configuration.objects.first():
            tracking_user_device(request)
        if user and not user.is_anonymous and user.is_authenticated and not user.first_login:
            UserDataManagementService(user).create_multiple_course_mngt_for_user()

        return Response(data={"success": True})


class SearchItem(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = request.user
        search = self.request.query_params.get("search", "").strip()
        return Response(data=response_search_item(search, ALL, user))
