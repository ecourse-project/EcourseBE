from django.db.models import Sum
from django.utils.timezone import localtime

from apps.courses.exceptions import NoItemException
from apps.documents.exceptions import NoDocumentException, CheckSaleStatusException
from apps.carts.exceptions import ListDocumentsEmptyException, ListCoursesEmptyException
from apps.carts.exceptions import (
    DocumentExistException,
    DocumentNotExistException,
    CourseExistException,
    CourseNotExistException,
)

from apps.carts.models import Cart
from apps.documents.api.serializers import DocumentManagementSerializer
from apps.documents.services.services import DocumentManagementService
from apps.documents.models import DocumentManagement
from apps.documents import enums as doc_enums
from apps.courses.api.serializers import CourseManagementSerializer
from apps.courses.services.services import CourseManagementService
from apps.courses.models import CourseManagement
from apps.courses import enums as course_enums


class CartService:
    def __init__(self, cart):
        self.cart = cart

    @property
    def custom_cart_data(self):
        cart = self.cart
        user = cart.user
        doc_mngt = DocumentManagementService(user).get_doc_management_queryset.filter(
            document__in=cart.documents.all()
        )
        course_mngt = CourseManagementService(user).get_course_management_queryset.filter(
            course__in=cart.courses.all()
        )
        return dict(
            id=cart.id,
            total_price=cart.total_price,
            documents=DocumentManagementSerializer(doc_mngt.order_by("-last_update"), many=True).data,
            courses=CourseManagementSerializer(course_mngt.order_by("-last_update"), many=True).data
        )

    def calculate_total_price(self):
        docs_price = Cart.objects.aggregate(total_price=Sum('documents__price'))['total_price']
        courses_price = Cart.objects.aggregate(total_price=Sum('courses__price'))['total_price']
        if not docs_price:
            docs_price = 0
        if not courses_price:
            courses_price = 0

        self.cart.total_price = docs_price + courses_price
        self.cart.save(update_fields=['total_price'])


class FavoriteListService:
    def __init__(self, favorite_list):
        self.favorite_list = favorite_list

    @property
    def custom_favorite_list_data(self):
        favorite_list = self.favorite_list
        user = favorite_list.user
        doc_mngt = DocumentManagementService(user).get_doc_management_queryset.filter(
            document__in=favorite_list.documents.all()
        )
        course_mngt = CourseManagementService(user).get_course_management_queryset.filter(
            course__in=favorite_list.courses.all()
        )
        return dict(
            id=favorite_list.id,
            documents=DocumentManagementSerializer(doc_mngt.order_by("-last_update"), many=True).data,
            courses=CourseManagementSerializer(course_mngt.order_by("-last_update"), many=True).data
        )


class MoveItems:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def validate_add_doc(cart, favorite_list, document):
        if favorite_list and cart:
            docs = favorite_list.documents.all()
            if not docs:
                raise ListDocumentsEmptyException
            if not docs.filter(id=document.id).exists():
                raise DocumentNotExistException
        elif cart:
            if cart.documents.all().filter(id=document.id).exists():
                raise DocumentExistException
        elif favorite_list:
            if favorite_list.documents.all().filter(id=document.id).exists():
                raise DocumentExistException

    @staticmethod
    def validate_remove_doc(cart, favorite_list, document):
        if cart:
            docs = cart.documents.all()
            if not docs:
                raise ListDocumentsEmptyException
            if not docs.filter(id=document.id).exists():
                raise DocumentNotExistException
        if favorite_list:
            docs = favorite_list.documents.all()
            if not docs:
                raise ListDocumentsEmptyException
            if not docs.filter(id=document.id).exists():
                raise DocumentNotExistException

    def move_doc(self, start, end, doc):
        if not doc:
            raise NoDocumentException
        cart = self.user.cart
        favorite_list = self.user.favorite_list
        doc_mngt = DocumentManagement.objects.get(user=self.user, document=doc)
        if doc_mngt.sale_status == doc_enums.PENDING or doc_mngt.sale_status == doc_enums.BOUGHT:
            raise CheckSaleStatusException

        if start.lower() == 'favorite' and end.lower() == 'cart':
            self.validate_add_doc(cart=cart, favorite_list=favorite_list, document=doc)
            cart.documents.add(doc)
            doc_mngt.sale_status = doc_enums.IN_CART
        elif start.lower() == 'list' and end.lower() == 'cart':
            self.validate_add_doc(cart=cart, favorite_list=None, document=doc)
            cart.documents.add(doc)
            doc_mngt.sale_status = doc_enums.IN_CART
        elif end.lower() == 'favorite':
            self.validate_add_doc(cart=None, favorite_list=favorite_list, document=doc)
            favorite_list.documents.add(doc)
            doc_mngt.is_favorite = True
        elif start.lower() == 'favorite' and end.lower() == 'list':
            self.validate_remove_doc(cart=None, favorite_list=favorite_list, document=doc)
            favorite_list.documents.remove(doc)
            doc_mngt.is_favorite = False
        elif start.lower() == 'cart' and end.lower() == 'list':
            self.validate_remove_doc(cart=cart, favorite_list=None, document=doc)
            cart.documents.remove(doc)
            doc_mngt.sale_status = doc_enums.AVAILABLE

        doc_mngt.last_update = localtime()
        doc_mngt.save(update_fields=['sale_status', 'is_favorite', 'last_update'])
        return doc_mngt

    @staticmethod
    def validate_add_course(cart, favorite_list, course):
        if cart and favorite_list:
            courses = favorite_list.courses.all()
            if not courses:
                raise ListCoursesEmptyException
            if not courses.filter(id=course.id).exists():
                raise CourseNotExistException
        elif cart:
            if cart.courses.all().filter(id=course.id).exists():
                raise CourseExistException
        elif favorite_list:
            if favorite_list.courses.all().filter(id=course.id).exists():
                raise CourseExistException

    @staticmethod
    def validate_remove_course(cart, favorite_list, course):
        if cart:
            courses = cart.courses.all()
            if not courses:
                raise ListCoursesEmptyException
            if not courses.filter(id=course.id).exists():
                raise CourseNotExistException
        if favorite_list:
            courses = favorite_list.courses.all()
            if not courses:
                raise ListCoursesEmptyException
            if not courses.filter(id=course.id).exists():
                raise CourseNotExistException

    def move_course(self, start, end, course):
        if not course:
            raise NoItemException
        cart = self.user.cart
        favorite_list = self.user.favorite_list
        course_mngt = CourseManagement.objects.get(user=self.user, course=course)
        if course_mngt.sale_status == course_enums.PENDING or course_mngt.sale_status == course_enums.BOUGHT:
            raise CheckSaleStatusException("Course has been checkout or bought.")

        if start.lower() == 'favorite' and end.lower() == 'cart':
            self.validate_add_course(cart=cart, favorite_list=favorite_list, course=course)
            cart.courses.add(course)
            course_mngt.sale_status = course_enums.IN_CART
        elif start.lower() == 'list' and end.lower() == 'cart':
            self.validate_add_course(cart=cart, favorite_list=None, course=course)
            cart.courses.add(course)
            course_mngt.sale_status = course_enums.IN_CART
        elif end.lower() == 'favorite':
            self.validate_add_course(cart=None, favorite_list=favorite_list, course=course)
            favorite_list.courses.add(course)
            course_mngt.is_favorite = True
        elif start.lower() == 'favorite' and end.lower() == 'list':
            self.validate_remove_course(cart=None, favorite_list=favorite_list, course=course)
            favorite_list.courses.remove(course)
            course_mngt.is_favorite = False
        elif start.lower() == 'cart' and end.lower() == 'list':
            self.validate_remove_course(cart=cart, favorite_list=None, course=course)
            cart.courses.remove(course)
            course_mngt.sale_status = course_enums.AVAILABLE

        course_mngt.last_update = localtime()
        course_mngt.save(update_fields=['sale_status', 'is_favorite', 'last_update'])
        return course_mngt
