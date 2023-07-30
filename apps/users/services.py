from apps.users.exceptions import MissedUsernameOrEmailException
from apps.users.models import User
from apps.documents.models import DocumentManagement
from apps.courses.models import CourseManagement


def exists_user(**kwargs):
    if not any(i for i in kwargs.values()):
        raise MissedUsernameOrEmailException()
    count = User.objects.filter(**{f"{field}__iexact": val for field, val in kwargs.items() if val}).count()
    return count > 0


def get_active_users():
    return User.objects.filter(is_active=True, is_superuser=False, last_login__isnull=False)


def get_users_to_create_course_mngt(course):
    if not course.course_of_class:
        return get_active_users().exclude(
            id__in=CourseManagement.objects.filter(
                course=course, course__course_of_class=False
            ).values_list("user_id", flat=True)
        )
    return User.objects.none()


def get_users_to_create_doc_mngt(document):
    return get_active_users().exclude(
        id__in=DocumentManagement.objects.filter(document=document).values_list("user_id", flat=True)
    )
