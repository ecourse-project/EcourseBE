from apps.rating.models import CourseRating
from apps.rating.api.serializers import RatingSerializer
from apps.users.models import User
from apps.quiz.models import Answer
from apps.courses.models import LessonManagement, VideoManagement, CourseDocumentManagement
from apps.classes.services.services import ClassRequestService
from apps.core.general import enums


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
                print(22222222222222222222222222222222222222222222222222)
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
