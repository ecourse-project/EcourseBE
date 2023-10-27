from apps.users.models import User
from apps.settings.enums import COURSE, CLASS
from apps.courses.models import CourseManagement
from apps.courses.enums import BOUGHT
from apps.classes.models import ClassManagement


def tracking_course_class_views(user: User, instance):
    if user.is_anonymous or not user.is_authenticated:
        return

    data = user.other_data if isinstance(user.other_data, dict) else {"docs": {}, "posts": {}, "classes": {}, "courses": {}}
    keys = list(data.keys())
    for item in ["docs", "posts", "classes", "courses"]:
        if item not in keys:
            data[item] = {}

    if isinstance(instance, CourseManagement) and instance.status == BOUGHT:
        course_data = data["courses"].get(str(instance.course_id), {"name": None, "views": 0, "type": COURSE})
        views = course_data.get("views", 0)
        data["courses"][str(instance.course_id)] = {
            "name": instance.course.name,
            "views": views + 1 if isinstance(views, int) else 1,
            "type": COURSE,
        }

    if isinstance(instance, ClassManagement) and instance.user_in_class:
        class_data = data["classes"].get(str(instance.course_id), {"name": None, "views": 0, "type": CLASS})
        views = class_data.get("views", 0)
        print(views)
        print(str(instance.course_id))
        data["classes"][str(instance.course_id)] = {
            "name": instance.course.name,
            "views": views + 1 if isinstance(views, int) else 1,
            "type": CLASS,
        }

    user.other_data = data
    user.save(update_fields=["other_data"])
