from datetime import datetime

from django.db.models import Sum, F

from apps.documents import enums as doc_enums
from apps.documents.models import DocumentManagement, Document
from apps.documents.api.serializers import DocumentManagementSerializer
from apps.documents.services.admin import DocumentAdminService
from apps.courses import enums as course_enums
from apps.courses.models import CourseManagement, Course
from apps.courses.api.serializers import CourseManagementSerializer
from apps.courses.services.admin import CourseAdminService
from apps.payment.enums import SUCCESS, FAILED
from apps.payment.models import Order

from apps.core.general.init_data import InitCourseServices


class OrderService:
    def __init__(self, order):
        self.order = order

    def add_documents(self, documents, user):
        if documents:
            self.order.documents.add(*documents)
            DocumentManagement.objects.filter(
                user=user,
                document__in=documents
            ).update(sale_status=doc_enums.PENDING)

    def add_courses(self, courses, user):
        if courses:
            self.order.courses.add(*courses)
            CourseManagement.objects.filter(
                user=user,
                course__in=courses
            ).update(sale_status=course_enums.PENDING)

    def cancel_order(self):
        DocumentManagement.objects.filter(
            user=self.order.user,
            document__in=self.order.documents.all()
        ).update(sale_status=doc_enums.AVAILABLE)
        CourseManagement.objects.filter(
            user=self.order.user,
            course__in=self.order.courses.all()
        ).update(sale_status=course_enums.AVAILABLE)

        self.order.status = FAILED
        self.order.save(update_fields=['status'])

    def custom_order_data(self, user):
        doc_mngt = DocumentManagement.objects.filter(
            user=user,
            document__in=self.order.documents.all()
        )
        course_mngt = CourseManagement.objects.filter(
            user=user,
            course__in=self.order.courses.all()
        )
        return dict(
            id=self.order.id,
            created=self.order.created,
            code=self.order.code,
            total_price=self.order.total_price,
            status=self.order.status,
            documents=DocumentManagementSerializer(doc_mngt, many=True).data,
            courses=CourseManagementSerializer(course_mngt, many=True).data
        )

    def order_success(self):
        doc_service = DocumentAdminService(self.order.user)
        course_service = CourseAdminService(self.order.user)
        """ Document """
        all_docs = self.order.documents.all()
        all_docs.update(sold=F('sold') + 1)
        doc_service.update_document_sale_status(all_docs, doc_enums.BOUGHT)

        """ Course """
        all_courses = self.order.courses.all()
        all_courses.update(sold=F('sold') + 1)
        course_service.update_course_sale_status(all_courses, course_enums.BOUGHT)
        for course in all_courses:
            InitCourseServices().init_course_data(course=course, user=self.order.user)
        course_service.enable_courses_data(all_courses)

    def order_failed(self):
        doc_service = DocumentAdminService(self.order.user)
        course_service = CourseAdminService(self.order.user)

        """ Document """
        doc_service.update_document_sale_status(self.order.documents.all(), doc_enums.AVAILABLE)

        """ Course """
        all_courses = self.order.courses.all()
        course_service.update_course_sale_status(all_courses, course_enums.AVAILABLE)
        course_service.disable_courses_data(all_courses)


# timestamp now - last 12 characters user id
def generate_code(user=None) -> str:
    timestamp = str(round(datetime.timestamp(datetime.now())))
    # user_id = str(user.id)
    # user_uuid_node = user_id[len(user_id) - 12:].upper()
    return f"{timestamp}"


def calculate_price(docs, courses) -> int:
    docs_price = Document.objects.filter(id__in=docs).aggregate(total=Sum('price'))['total']
    courses_price = Course.objects.filter(id__in=courses).aggregate(total=Sum('price'))['total']
    if not docs_price:
        docs_price = 0
    if not courses_price:
        courses_price = 0
    return docs_price + courses_price
