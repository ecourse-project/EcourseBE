from django.db.models import Q

from apps.rating.models import CourseRating
from apps.rating.api.serializers import RatingSerializer
from apps.users.models import User
from apps.core.general import enums
from apps.settings.enums import ALL, DOCUMENT, COURSE, CLASS, POST

from apps.documents.models import Document
from apps.courses.models import (
    LessonManagement,
    VideoManagement,
    CourseDocumentManagement,
    Course,
    LessonQuizManagement,
)
# from apps.classes.models import Class
from apps.posts.models import Post
from apps.classes.services.services import ClassRequestService
from apps.quiz.services.services import (
    quiz_statistic,
    response_quiz_statistic,
)
from apps.quiz.services.queryset_services import get_quiz_queryset
from apps.quiz.api.serializers import QuizManagementSerializer
from apps.quiz.enums import (
    QUESTION_TYPE_CHOICES,
    QUESTION_TYPE_MATCH,
    QUESTION_TYPE_FILL,
)


class CustomListDataServices:
    def __init__(self, user: User):
        self.user = user
        self.class_request_service = ClassRequestService()
        self.dict_data_service = CustomDictDataServices(user=user)

    def custom_response_list_data(self, data: list, **kwargs):
        fields = kwargs.get("fields", [])
        data = self.filter_available_course_document(data)
        data = self.filter_available_video(data)

        for field in fields:
            if field == enums.REQUEST_STATUS and kwargs.get("class_objs"):
                data = self.class_request_service.add_request_status(data, field, self.user, kwargs.get("class_objs"))
            if field == enums.QUIZ_DETAIL:
                data = self.add_quiz_detail(data, field)
            if field == enums.LIST_QUIZ:
                data = self.add_list_quiz(data, field)
            if field == enums.IS_DONE_QUIZ:
                data = self.add_is_done_quiz(data, field)
        return data

    def filter_available_course_document(self, data: list):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.filter_available_course_document(dt)
        return data

    def filter_available_video(self, data: list):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.filter_available_video(dt)
        return data

    def add_docs_videos_completed(self, data: list, doc_field: str, video_field: str):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.add_docs_videos_completed(dt, doc_field, video_field)
        return data

    def add_is_done_quiz(self, data: dict, field: str):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.add_is_done_quiz(dt, field)
        return data

    def add_quiz_detail(self, data: list, field: str):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.add_quiz_detail(dt, field)
        return data

    def add_list_quiz(self, data: list, field: str):
        for index, dt in enumerate(data):
            data[index] = self.dict_data_service.add_list_quiz(dt, field)
        return data


class CustomDictDataServices:
    def __init__(self, user: User):
        self.user = user
        self.class_request_service = ClassRequestService()

    def custom_response_dict_data(self, data: dict, **kwargs):
        fields = kwargs.get("fields", [])
        data = self.filter_available_course_document(data)
        data = self.filter_available_video(data)

        if enums.DOCS_COMPLETED in fields and enums.VIDEOS_COMPLETED in fields:
            data = self.add_docs_videos_completed(data, enums.DOCS_COMPLETED, enums.VIDEOS_COMPLETED)

        for field in fields:
            if field == enums.REQUEST_STATUS and kwargs.get("class_objs"):
                data = self.class_request_service.add_request_status(data, field, self.user, kwargs.get("class_objs"))
            if field == enums.QUIZ_DETAIL:
                data = self.add_quiz_detail(data, field)
            if field == enums.LIST_QUIZ:
                data = self.add_list_quiz(data, field)
            if field == enums.IS_DONE_QUIZ:
                data = self.add_is_done_quiz(data, field)

        return data

    def filter_available_course_document(self, data: dict):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            lesson_docs = [doc.get("id") for doc in lesson.get("documents", [])]
            if not lesson_docs:
                continue
            available_docs = CourseDocumentManagement.objects.filter(
                user=self.user,
                course_id=data['id'],
                lesson_id=lesson['id'],
                document_id__in=lesson_docs,
                is_available=True,
            ).values_list("document_id", flat=True)
            available_docs = [str(doc_id) for doc_id in available_docs]
            data["lessons"][index]["documents"] = [
                doc for doc in data["lessons"][index]["documents"] if doc.get("id") in available_docs
            ]

        return data

    def filter_available_video(self, data: dict):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            lesson_videos = [video.get("id") for video in lesson.get("videos", [])]
            if not lesson_videos:
                continue
            available_videos = VideoManagement.objects.filter(
                user=self.user,
                course_id=data['id'],
                lesson_id=lesson['id'],
                video_id__in=lesson_videos,
                is_available=True,
            ).values_list("video_id", flat=True)
            available_videos = [str(video_id) for video_id in available_videos]
            data["lessons"][index]["videos"] = [
                video for video in data["lessons"][index]["videos"] if video.get("id") in available_videos
            ]

        return data

    def add_docs_videos_completed(self, data: dict, doc_field: str, video_field: str):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            lesson_mngt = LessonManagement.objects.filter(lesson_id=lesson['id']).first()
            if lesson_mngt:
                lesson_obj = lesson_mngt.lesson
                data["lessons"][index][doc_field] = (
                    CourseDocumentManagement.objects.filter(
                        user=self.user,
                        course_id=data['id'],
                        lesson_id=lesson['id'],
                        document__in=lesson_obj.documents.all(),
                        is_completed=True,
                        is_available=True,
                    ).values_list("document", flat=True)
                )
                data["lessons"][index][video_field] = (
                    VideoManagement.objects.filter(
                        user=self.user,
                        course_id=data["id"],
                        lesson_id=lesson['id'],
                        video__in=lesson_obj.videos.all(),
                        is_completed=True,
                        is_available=True,
                    ).values_list("video", flat=True)
                )
            else:
                data["lessons"][index][doc_field] = []
                data["lessons"][index][video_field] = []

        return data

    # TODO: Optimize by query
    def add_is_done_quiz(self, data: dict, field: str):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            lesson_quiz = LessonQuizManagement.objects.filter(
                course_mngt__user=self.user,
                course_mngt__course_id=data['id'],
                lesson_id=lesson['id']
            ).first()
            data["lessons"][index][field] = lesson_quiz.is_done_quiz if lesson_quiz else False

        return data

    def add_quiz_detail(self, data: dict, field: str):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            lesson_quiz_mngt = LessonQuizManagement.objects.filter(
                course_mngt__user=self.user, course_mngt__course_id=data["id"], lesson_id=lesson["id"]
            ).first()
            if lesson_quiz_mngt and lesson_quiz_mngt.is_done_quiz and lesson_quiz_mngt.date_done_quiz:
                data["lessons"][index][field] = response_quiz_statistic(
                    quiz_statistic(
                        user=self.user,
                        course_id=data['id'],
                        lesson_id=lesson["id"],
                        created=lesson_quiz_mngt.date_done_quiz,
                    )
                )
        return data

    def add_list_quiz(self, data: dict, field: str):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            data["lessons"][index][field] = (
                QuizManagementSerializer(
                    get_quiz_queryset().filter(
                        Q(
                            Q(course_id=data['id'], lesson_id=lesson["id"])
                            & Q(
                                Q(question_type=QUESTION_TYPE_CHOICES, choices_question__isnull=False)
                                | Q(question_type=QUESTION_TYPE_MATCH, match_question__isnull=False)
                                | Q(question_type=QUESTION_TYPE_FILL, fill_blank_question__isnull=False)
                            )
                        )
                    ),
                    many=True,
                ).data
            )
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

    return response


