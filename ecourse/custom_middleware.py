import pytz

from django.utils import timezone
from apps.configuration.models import Configuration
from apps.core.system import tracking_user


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate(pytz.timezone('Asia/Ho_Chi_Minh'))
        return self.get_response(request)


class TrackingMiddleware:
    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request):
        config = Configuration.objects.first()
        if config.user_tracking and request.path.startswith("/api"):
            tracking_user(request)
        return self.get_request(request)
