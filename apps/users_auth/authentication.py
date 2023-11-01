from rest_framework.permissions import BasePermission

from apps.users_auth.services import update_user_ip
from apps.users_auth.choices import LIMIT_IP_PATH
from apps.users.choices import MANAGER
from apps.users.services import tracking_user_api

from apps.configuration.models import Configuration

from ipware import get_client_ip


class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        has_permission = bool(user and user.is_authenticated)
        config = Configuration.objects.first()

        # Tracking api
        if config.tracking_api:
            tracking_user_api(request)

        # Tracking IP address
        if config.tracking_ip and request.path in LIMIT_IP_PATH:
            current_ip = get_client_ip(request)
            if current_ip and (isinstance(current_ip, list) or isinstance(current_ip, tuple)):
                update_user_ip(user, current_ip[0])
                user.save(update_fields=["ip_addresses", "unverified_ip_addresses"])

        return has_permission


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            True if (
                not request.user.is_anonymous
                and request.user.is_authenticated
                and request.user.role == MANAGER
            )
            else False
        )
