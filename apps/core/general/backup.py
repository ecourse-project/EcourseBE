from apps.documents.models import DocumentManagement, Document
from apps.documents import enums as doc_enums
from apps.courses.models import CourseManagement, Course
from apps.courses import enums as course_enums
from apps.users.models import UserDataBackUp
from apps.users.choices import MANAGER


def store_backup_user_data(user):
    documents = DocumentManagement.objects.filter(user=user)
    documents_data = {
        str(d.document_id): {
            "name": d.document.name,
            "sale_status": d.sale_status,
        }
        for d in documents
    } if documents else None

    courses = CourseManagement.objects.filter(user=user)
    courses_data = {
        str(c.course_id): {
            "name": c.course.name,
            "sale_status": c.sale_status,
            "user_in_class": True if c.user_in_class else False,
        }
        for c in courses
    } if courses else None

    if not documents_data and not courses_data:
        return documents_data, courses_data

    backup_obj, _ = UserDataBackUp.objects.get_or_create(user=user)
    backup_obj.documents = documents_data
    backup_obj.courses = courses_data
    backup_obj.save(update_fields=["documents", "courses"])

    return documents_data, courses_data


def update_manager_document_mngt(user):
    all_doc = Document.objects.all()
    user_doc = DocumentManagement.objects.filter(user=user)
    docs_mngt_to_create = all_doc.values_list("id", flat=True).difference(user_doc.values_list("document_id", flat=True))

    if docs_mngt_to_create:
        DocumentManagement.objects.bulk_create([
            DocumentManagement(
                document_id=doc_id, user=user, sale_status=doc_enums.BOUGHT
            ) for doc_id in docs_mngt_to_create
        ])
    user_doc.update(sale_status=doc_enums.BOUGHT)


def update_manager_course_mngt(user):
    all_course = Course.objects.all()
    user_course = CourseManagement.objects.filter(user=user)
    courses_mngt_to_create = all_course.values_list("id", flat=True).difference(user_course.values_list("course_id", flat=True))

    if courses_mngt_to_create:
        CourseManagement.objects.bulk_create([
            CourseManagement(
                course_id=course_id, user=user, sale_status=course_enums.BOUGHT, user_in_class=True
            ) for course_id in courses_mngt_to_create
        ])
    user_course.update(sale_status=doc_enums.BOUGHT, user_in_class=True)


def backup_document_mngt(user, docs: dict):
    document_mngt = DocumentManagement.objects.filter(user=user)

    if not docs or not isinstance(docs, dict):
        return

    docs_to_update = []
    for doc in document_mngt:
        if docs.get(str(doc.document_id)):
            doc.sale_status = docs[str(doc.document_id)]["sale_status"]
            docs_to_update.append(doc)

    DocumentManagement.objects.bulk_update(docs_to_update, fields=["sale_status"])


def backup_course_mngt(user, courses: dict):
    course_mngt = CourseManagement.objects.filter(user=user)

    if not courses or not isinstance(courses, dict):
        return

    courses_to_update = []
    for course in course_mngt:
        if courses.get(str(course.course_id)):
            course.sale_status = courses[str(course.course_id)]["sale_status"]
            course.user_in_class = courses[str(course.course_id)]["user_in_class"]
            courses_to_update.append(course)

    CourseManagement.objects.bulk_update(courses_to_update, fields=["sale_status", "user_in_class"])


def change_user_role(user, current, to_role):
    if current != MANAGER and to_role == MANAGER:
        store_backup_user_data(user)
        update_manager_document_mngt(user)
        update_manager_course_mngt(user)
    elif current == MANAGER and to_role != MANAGER:
        backup = UserDataBackUp.objects.filter(user=user).first()
        if not backup:
            return
        backup_document_mngt(user, backup.documents)
        backup_course_mngt(user, backup.courses)
        backup.documents = None
        backup.courses = None
        backup.save(update_fields=["documents", "courses"])
