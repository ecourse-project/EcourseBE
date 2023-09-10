from rest_framework.permissions import BasePermission

from apps.users_auth.services import update_user_ip
from apps.users_auth.choices import LIMIT_IP_PATH
from apps.configuration.models import Configuration

from ipware import get_client_ip


class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        has_permission = bool(user and request.user.is_authenticated)
        if request.path in LIMIT_IP_PATH:
            current_ip = get_client_ip(request)[0]
            update_user_ip(user, current_ip)
            user.save(update_fields=["ip_addresses", "unverified_ip_addresses"])

        return has_permission
