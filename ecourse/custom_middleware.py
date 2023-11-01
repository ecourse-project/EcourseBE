import pytz

from django.utils import timezone
from django.conf import settings


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate(pytz.timezone(settings.TIME_ZONE))
        return self.get_response(request)
