from apps.configuration.models import Configuration
from apps.users.models import User
from apps.users_auth.exceptions import PermissionException


def update_user_ip(user: User, ip_address):
    config = Configuration.objects.first()
    user_ip = user.ip_addresses or []
    if ip_address in user_ip:
        return
    else:
        user_unverified_ip = user.unverified_ip_addresses or []
        if not config.unlimited_ip_addresses and len(user_ip) >= config.ip_address_limit:
            user.unverified_ip_addresses = list(set(user_unverified_ip + [ip_address]))
            user.save(update_fields=["unverified_ip_addresses"])
            raise PermissionException()
        else:
            user.ip_addresses = list(set(user_ip + [ip_address]))
            if ip_address in user_unverified_ip:
                user_unverified_ip.remove(ip_address)
                user.unverified_ip_addresses = user_unverified_ip or None
