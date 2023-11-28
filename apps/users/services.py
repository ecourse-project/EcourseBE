import json
from ipware import get_client_ip

from apps.users.exceptions import MissedUsernameOrEmailException
from apps.users.models import User, UserTracking, DeviceTracking
from apps.users.choices import DEVICE_MOBILE, DEVICE_TABLET, DEVICE_PC

from apps.documents.models import DocumentManagement
from apps.courses.models import CourseManagement
from apps.classes.models import ClassManagement


def exists_user(**kwargs):
    if not any(i for i in kwargs.values()):
        raise MissedUsernameOrEmailException()
    count = User.objects.filter(**{f"{field}__iexact": val for field, val in kwargs.items() if val}).count()
    return count > 0


def get_active_users():
    return User.objects.filter(
        is_active=True,
        is_superuser=False,
        # is_staff=False,
        last_login__isnull=False,
    )


def tracking_user_api(request):
    post_data = request.body.decode('utf-8')
    try:
        data = json.loads(post_data)
    except Exception:
        data = None

    ip_address = get_client_ip(request)
    ip_address = (
        ip_address[0]
        if ip_address and (isinstance(ip_address, list) or isinstance(ip_address, tuple))
        else None
    )

    user = request.user
    user = user if user and user.is_authenticated and not user.is_anonymous else None

    UserTracking.objects.create(
        user=user,
        method=request.method,
        ip_address=ip_address,
        path=request.path,
        query_params=request.GET.dict() or None,
        data=data,
    )


def tracking_user_device(request):
    user = request.user
    if user.is_anonymous or not user.is_authenticated:
        return

    device_type = None
    if request.user_agent.is_mobile:
        device_type = DEVICE_MOBILE
    elif request.user_agent.is_tablet:
        device_type = DEVICE_TABLET
    elif request.user_agent.is_pc:
        device_type = DEVICE_PC

    DeviceTracking.objects.create(
        user=user,
        device_type=device_type,
        device=request.user_agent.device.family,
        browser=request.user_agent.browser.family,
        browser_version=request.user_agent.browser.version_string,
        system=request.user_agent.os.family,
        system_version=request.user_agent.os.version_string,
    )


def get_users_to_create_course_mngt(course):
    if course.course_of_class:
        return get_active_users().exclude(
            id__in=ClassManagement.objects.filter(
                course=course, course__course_of_class=True
            ).values_list("user_id", flat=True)
        )
    else:
        return get_active_users().exclude(
            id__in=CourseManagement.objects.filter(
                course=course, course__course_of_class=False
            ).values_list("user_id", flat=True)
        )


def get_users_to_create_doc_mngt(document):
    return get_active_users().exclude(
        id__in=DocumentManagement.objects.filter(document=document).values_list("user_id", flat=True)
    )
