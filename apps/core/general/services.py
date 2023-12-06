from django.db.models import Q

from apps.users.models import User
from apps.users.choices import TEACHER

from apps.rating.models import CourseRating
from apps.rating.api.serializers import RatingSerializer

from apps.documents.models import Document
from apps.documents.services.services import DocumentManagementService

from apps.courses.models import (
    Course,
    Lesson,
    QuizManagement,
    CourseManagement,
    LessonManagement,
    CourseDocumentManagement,
    VideoManagement,
)
from apps.courses.api.serializers import ListCourseManagementSerializer
from apps.courses.services.services import CourseService, CourseManagementService

from apps.posts.models import Post
from apps.posts.services.services import PostsService

from apps.classes.services.services import ClassesService
from apps.classes.services.services import ClassRequestService

from apps.quiz.models import Quiz
from apps.quiz.services.services import (
    quiz_statistic,
    response_quiz_statistic,
)
from apps.quiz.services.queryset_services import get_quiz_queryset
from apps.quiz.api.serializers import QuizSerializer
from apps.quiz.enums import (
    QUESTION_TYPE_CHOICES,
    QUESTION_TYPE_MATCH,
    QUESTION_TYPE_FILL,
)

from apps.upload.api.serializers import UploadImageSerializer
from apps.core.general import enums


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
        self.course_service = CourseService()

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
                enable=True,
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
                enable=True,
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
                condition = Q(
                    user=self.user, course_id=data['id'], lesson_id=lesson['id'],
                    is_completed=True, is_available=True, enable=True,
                )
                data["lessons"][index][doc_field] = (
                    CourseDocumentManagement.objects.filter(
                        condition & Q(document__in=lesson_obj.documents.all())
                    ).values_list("document_id", flat=True)
                )
                data["lessons"][index][video_field] = (
                    VideoManagement.objects.filter(
                        condition & Q(video__in=lesson_obj.videos.all())
                    ).values_list("video_id", flat=True)
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
            lesson_quiz = QuizManagement.objects.filter(
                course_mngt__user=self.user,
                course_mngt__course_id=data['id'],
                lesson_id=lesson['id']
            ).first()
            data["lessons"][index][field] = lesson_quiz.is_done_quiz if lesson_quiz else False

        return data

    # User result
    def add_quiz_detail(self, data: dict, field: str):
        if not data.get("lessons"):
            return data

        quiz_location_update = {}
        for index, lesson in enumerate(data["lessons"], start=0):
            quiz_location = lesson["quiz_location"]
            if not quiz_location or not isinstance(quiz_location, list):
                continue

            quiz_detail = []
            list_idx_remove = []
            for idx, quiz in enumerate(quiz_location):
                if not isinstance(quiz, dict) or (isinstance(quiz, dict) and not quiz.get("id")):
                    continue
                elif not Quiz.objects.filter(pk=quiz["id"]).exists():
                    list_idx_remove.append(idx)
                    continue

                quiz_mngt, _ = QuizManagement.objects.get_or_create(
                    user=self.user,
                    course_id=data["id"],
                    lesson_id=lesson["id"],
                    quiz_id=quiz["id"],
                )

                if quiz_mngt and quiz_mngt.is_done_quiz and quiz_mngt.date_done_quiz:
                    quiz_info = (
                        response_quiz_statistic(
                            quiz_statistic(
                                quiz_id=quiz["id"],
                                user=self.user,
                                created=quiz_mngt.date_done_quiz
                            )
                        )
                    )
                    quiz_detail.append({**quiz_info, **{"is_done_quiz": quiz_mngt.is_done_quiz}})

            data["lessons"][index][field] = quiz_detail
            if list_idx_remove:
                [quiz_location.pop(idx) for idx in list_idx_remove]
                quiz_location_update[lesson["id"]] = quiz_location

        # Update quiz_location if quiz is removed
        lessons = Lesson.objects.filter(pk__in=quiz_location_update.keys())
        for lesson in lessons:
            lesson.quiz_location = quiz_location_update[str(lesson.pk)]
        Lesson.objects.bulk_update(lessons, fields=["quiz_location"])

        return data

    # Quiz info
    def add_list_quiz(self, data: dict, field: str):
        if not data.get("lessons"):
            return data

        for index, lesson in enumerate(data["lessons"], start=0):
            if not lesson["quiz_location"] or not isinstance(lesson["quiz_location"], list):
                continue

            list_quiz_id = [obj["id"] for obj in lesson["quiz_location"]]
            data["lessons"][index][field] = (
                QuizSerializer(
                    instance=get_quiz_queryset().filter(pk__in=list_quiz_id),
                    many=True
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


def search_item_active_user(item_name: str, search_type: str, user: User) -> dict:
    response = {"documents": [], "courses": [], "classes": [], "posts": []}
    if search_type.upper() not in [enums.ALL, enums.DOCUMENT, enums.COURSE, enums.CLASS, enums.POST]:
        return response
    if isinstance(item_name, str):
        item_name = item_name.strip()

    doc_service = DocumentManagementService(user)
    course_service = CourseManagementService(user)
    class_service = ClassesService()
    post_service = PostsService()

    if search_type.upper() == enums.ALL:
        response["documents"] = (
            doc_service
            .get_doc_mngt_queryset_by_selling
            .filter(document__name__icontains=item_name)
            .values_list("document_id", flat=True)
        )
        response["courses"] = (
            course_service
            .get_course_mngt_queryset_by_selling
            .filter(course__name__icontains=item_name)
            .values_list("course_id", flat=True)
        )
        response["classes"] = (
            class_service
            .get_all_classes_queryset
            .filter(name__icontains=item_name)
            .values_list("id", flat=True)
        )
        response["posts"] = (
            post_service
            .get_all_posts_queryset
            .filter(name__icontains=item_name)
            .values_list("id", flat=True)
        )

    elif search_type.upper() == enums.DOCUMENT:
        response["documents"] = (
            doc_service
            .get_doc_mngt_queryset_by_selling
            .filter(document__name__icontains=item_name)
            .values_list("document_id", flat=True)
        )
    elif search_type.upper() == enums.COURSE:
        response["courses"] = (
            course_service
            .get_course_mngt_queryset_by_selling
            .filter(course__name__icontains=item_name)
            .values_list("course_id", flat=True)
        )
    elif search_type.upper() == enums.CLASS:
        response["classes"] = (
            class_service
            .get_all_classes_queryset
            .filter(name__icontains=item_name)
            .values_list("id", flat=True)
        )
    elif search_type.upper() == enums.POST:
        response["posts"] = (
            post_service
            .get_all_posts_queryset
            .filter(name__icontains=item_name)
            .values_list("id", flat=True)
        )

    return response


def search_item_anonymous_user(item_name: str, search_type: str) -> dict:
    response = {"documents": [], "courses": [], "classes": [], "posts": []}
    if search_type.upper() not in [enums.ALL, enums.DOCUMENT, enums.COURSE, enums.CLASS, enums.POST]:
        return response
    if isinstance(item_name, str):
        item_name = item_name.strip()

    if search_type.upper() == enums.ALL:
        response["documents"] = Document.objects.filter(name__icontains=item_name, is_selling=True)
        response["courses"] = Course.objects.filter(name__icontains=item_name, is_selling=True, course_of_class=False)
        response["classes"] = Course.objects.filter(name__icontains=item_name, course_of_class=True)
        response["posts"] = Post.objects.filter(name__icontains=item_name)

    elif search_type.upper() == enums.DOCUMENT:
        response["documents"] = response["documents"] = Document.objects.filter(name__icontains=item_name, is_selling=True)
    elif search_type.upper() == enums.COURSE:
        response["courses"] = Course.objects.filter(name__icontains=item_name, is_selling=True, course_of_class=False)
    elif search_type.upper() == enums.CLASS:
        response["classes"] = Course.objects.filter(name__icontains=item_name, course_of_class=True)
    elif search_type.upper() == enums.POST:
        response["posts"] = Post.objects.filter(name__icontains=item_name)

    return response


def response_search_item(item_name: str, search_type: str, user: User):
    if user and user.is_authenticated:
        response = search_item_active_user(item_name, search_type, user)
        documents = Document.objects.filter(pk__in=response["documents"])
        courses = Course.objects.filter(pk__in=response["courses"])
        classes = Course.objects.filter(pk__in=response["classes"])
        posts = Post.objects.filter(pk__in=response["posts"])
    else:
        response = search_item_anonymous_user(item_name, search_type)
        documents = response["documents"]
        courses = response["courses"]
        classes = response["classes"]
        posts = response["posts"]

    return [
        *[
            {
                "id": str(doc.id),
                "author": doc.author.full_name if doc.author and doc.author.role == TEACHER else "",
                "name": doc.name,
                "thumbnail": UploadImageSerializer(instance=doc.thumbnail).data,
                "content_summary": "",
                "type": enums.DOCUMENT,
            }
            for doc in documents
        ],
        *[
            {
                "id": str(course.id),
                "author": course.author.full_name if course.author and course.author.role == TEACHER else "",
                "name": course.name,
                "thumbnail": UploadImageSerializer(instance=course.thumbnail).data,
                "type": enums.COURSE,
            }
            for course in courses
        ],
        *[
            {
                "id": str(cls.id),
                "author": cls.author.full_name if cls.author and cls.author.role == TEACHER else "",
                "name": cls.name,
                "thumbnail": UploadImageSerializer(instance=cls.thumbnail).data,
                "type": enums.CLASS,
            }
            for cls in classes
        ],
        *[
            {
                "id": str(post.id),
                "author": post.author.full_name if post.author and post.author.role == TEACHER else "",
                "name": post.name,
                "thumbnail": UploadImageSerializer(instance=post.thumbnail).data,
                "content_summary": post.content_summary,
                "type": enums.POST,
            }
            for post in posts
        ]
    ]


def check_existing_instance(model_class, **kwargs):
    return True if model_class.objects.filter(**kwargs).exists() else False
