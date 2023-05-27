from django.db.models import QuerySet, Q

from apps.rating.models import CourseRating
from apps.rating.api.serializers import RatingSerializer
from apps.users.models import User
from apps.quiz.models import Answer
from apps.core.general import enums
from apps.settings.enums import ALL, DOCUMENT, COURSE, CLASS, POST

from apps.documents.models import Document
from apps.courses.models import LessonManagement, VideoManagement, CourseDocumentManagement, Course
from apps.classes.models import Class
from apps.posts.models import Post

from apps.documents.api.serializers import DocumentSerializer, DocumentManagementSerializer
from apps.courses.api.serializers import ListCourseSerializer, ListCourseManagementSerializer
from apps.classes.api.serializers import ListClassSerializer
from apps.posts.api.serializers import PostSerializer

from apps.documents.services.services import DocumentService
from apps.courses.services.services import CourseService
from apps.classes.services.services import ClassesService
from apps.posts.services.services import PostsService
from apps.classes.services.services import ClassRequestService


class CustomListDataServices:
    def __init__(self, user: User):
        self.user = user
        self.class_request_service = ClassRequestService()
        self.dict_data_service = CustomDictDataServices(user=user)

    def custom_response_list_data(self, data: list, **kwargs):
        fields = kwargs.get("fields", [])

        for field in fields:
            if field == enums.REQUEST_STATUS and kwargs.get("class_objs"):
                data = self.class_request_service.add_request_status(data, field, self.user, kwargs.get("class_objs"))
            if field == enums.QUIZ_DETAIL:
                data = self.add_quiz_detail(data, field)
        return data

    def add_docs_videos_completed(self, data: list, doc_field: str, video_field: str):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.add_docs_videos_completed(dt, doc_field, video_field)
        return data

    def add_quiz_detail(self, data: list, field: str):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.add_quiz_detail(dt, field)
        return data


class CustomDictDataServices:
    def __init__(self, user: User):
        self.user = user
        self.class_request_service = ClassRequestService()

    def custom_response_dict_data(self, data: dict, **kwargs):
        fields = kwargs.get("fields", [])
        if enums.DOCS_COMPLETED in fields and enums.VIDEOS_COMPLETED in fields:
            data = self.add_docs_videos_completed(data, enums.DOCS_COMPLETED, enums.VIDEOS_COMPLETED)

        for field in fields:
            if field == enums.REQUEST_STATUS and kwargs.get("class_objs"):
                data = self.class_request_service.add_request_status(data, field, self.user, kwargs.get("class_objs"))
            if field == enums.QUIZ_DETAIL:
                data = self.add_quiz_detail(data, field)
        return data

    def add_docs_videos_completed(self, data: dict, doc_field: str, video_field: str):
        for index, lesson in enumerate(data["lessons"], start=0):
            lesson_mngt = LessonManagement.objects.filter(lesson_id=lesson['id']).first()
            if lesson_mngt:
                lesson_obj = lesson_mngt.lesson
                data["lessons"][index][doc_field] = (
                    CourseDocumentManagement.objects.filter(
                        user=self.user,
                        course_id=data['id'],
                        document__in=lesson_obj.documents.all(),
                        is_completed=True,
                        is_available=True,
                    ).values_list("document", flat=True)
                )
                data["lessons"][index][video_field] = (
                    VideoManagement.objects.filter(
                        user=self.user,
                        course_id=data["id"],
                        video__in=lesson_obj.videos.all(),
                        is_completed=True,
                        is_available=True,
                    ).values_list("video", flat=True)
                )
            else:
                data["lessons"][index][doc_field] = []
                data["lessons"][index][video_field] = []

        return data

    def add_quiz_detail(self, data: dict, field: str):
        quiz_detail = {}
        quiz_answers = []
        correct_answers = 0
        total_answers = Answer.objects.filter(quiz__course_id=data['id'], user=self.user)

        for answer in total_answers:
            quiz_answers.append({
                "quiz_id": answer.quiz_id,
                "answer_choice": answer.choice,
                "correct_answer": answer.quiz.correct_answer.choice
            })
            if answer.choice == answer.quiz.correct_answer.choice:
                correct_answers += 1

        quiz_detail["correct_answers"] = correct_answers
        quiz_detail["total_quiz"] = len(total_answers)
        quiz_detail["quiz_answers"] = quiz_answers
        data[field] = quiz_detail

        return data

    def add_rating(self, data: dict, field: str):
        course_rating = CourseRating.objects.filter(course_id=data['id']).first()
        all_ratings = course_rating.ratings.all()
        my_rating = course_rating.ratings.filter(user=self.user).first()
        data['rating_detail'] = RatingSerializer(all_ratings, many=True).data if all_ratings else []
        data['my_rating'] = RatingSerializer(my_rating).data if my_rating else {}

        response = {}
        for score in range(1, 6):
            response["score_" + str(score)] = all_ratings.filter(rating=score).count()
        data[field] = response


def search_item(item_name: str, search_type: str, user: User) -> dict:
    response = {"documents": [], "courses": [], "classes": [], "posts": []}
    if search_type.upper() not in [ALL, DOCUMENT, COURSE, CLASS, POST]:
        return response

    if search_type.upper() == ALL:
        response["documents"] = Document.objects.filter(name__icontains=item_name, is_selling=True).values_list("id", flat=True)
        response["courses"] = Course.objects.filter(
            name__icontains=item_name, is_selling=True, course_of_class=False
        ).values_list("id", flat=True)
        response["classes"] = Course.objects.filter(name__icontains=item_name, course_of_class=True).values_list("id", flat=True)
        response["posts"] = Post.objects.filter(name__icontains=item_name).values_list("id", flat=True)

    elif search_type.upper() == DOCUMENT:
        response["documents"] = Document.objects.filter(name__icontains=item_name, is_selling=True).values_list("id", flat=True)

    elif search_type.upper() == COURSE:
        response["courses"] = Course.objects.filter(
            name__icontains=item_name, is_selling=True, course_of_class=False
        ).values_list("id", flat=True)

    elif search_type.upper() == CLASS:
        response["classes"] = Course.objects.filter(name__icontains=item_name, course_of_class=True).values_list("id", flat=True)

    elif search_type.upper() == POST:
        response["posts"] = Post.objects.filter(name__icontains=item_name).values_list("id", flat=True)

    # if search_type.upper() == ALL:
    #     documents = DocumentService().get_all_documents_queryset.filter(name__icontains=item_name)
    #     courses = CourseService().get_all_courses_queryset.filter(name__icontains=item_name)
    #     classes = ClassesService().get_all_classes_queryset.filter(name__icontains=item_name)
    #     if user.is_anonymous or not user.is_authenticated:
    #         response["documents"] = DocumentSerializer(documents, many=True).data
    #         response["courses"] = ListCourseSerializer(courses, many=True).data
    #         response["classes"] = ListClassSerializer(classes, many=True).data
    #     else:
    #         response["documents"] = DocumentManagementSerializer(documents, many=True).data
    #         response["courses"] = ListCourseManagementSerializer(courses, many=True).data
    #         response["classes"] = CustomListDataServices(user=user).custom_response_list_data(
    #             data=ListClassSerializer(classes, many=True).data,
    #             fields=[enums.REQUEST_STATUS],
    #             user=user,
    #             class_objs=classes,
    #         )
    #     response["posts"] = PostSerializer(PostsService().get_all_posts_queryset.filter(name__icontains=item_name), many=True).data
    #
    # elif search_type.upper() == DOCUMENT:
    #     documents = DocumentService().get_all_documents_queryset.filter(name__icontains=item_name)
    #     if user.is_anonymous or not user.is_authenticated:
    #         response["documents"] = DocumentSerializer(documents, many=True).data
    #     else:
    #         response["documents"] = DocumentManagementSerializer(documents, many=True).data
    #
    # elif search_type.upper() == COURSE:
    #     courses = CourseService().get_all_courses_queryset.filter(name__icontains=item_name)
    #     if user.is_anonymous or not user.is_authenticated:
    #         response["courses"] = ListCourseSerializer(courses, many=True).data
    #     else:
    #         response["courses"] = ListCourseManagementSerializer(courses, many=True).data
    #
    # elif search_type.upper() == CLASS:
    #     classes = ClassesService().get_all_classes_queryset.filter(name__icontains=item_name)
    #     if user.is_anonymous or not user.is_authenticated:
    #         response["classes"] = ListClassSerializer(classes, many=True).data
    #     else:
    #         response["classes"] = CustomListDataServices(user=user).custom_response_list_data(
    #             data=ListClassSerializer(classes, many=True).data,
    #             fields=[enums.REQUEST_STATUS],
    #             user=user,
    #             class_objs=classes,
    #         )
    #
    # elif search_type.upper() == POST:
    #     response["posts"] = PostSerializer(
    #         PostsService().get_all_posts_queryset.filter(name__icontains=item_name), many=True
    #     ).data

    return response



