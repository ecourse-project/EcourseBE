from django.db.models import Prefetch, Q
from django.utils.timezone import localtime

from apps.courses.models import (
    Course,
    Lesson,
    CourseDocument,
    CourseManagement,
    LessonManagement,
    CourseDocumentManagement,
    VideoManagement,
)
from apps.courses.enums import BOUGHT, PENDING
from apps.rating.api.serializers import RatingSerializer
from apps.rating.models import CourseRating
from apps.quiz.models import Answer


class CourseService:
    @property
    def get_all_courses_queryset(self):
        return Course.objects.prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file")))
                     )
        ).select_related('topic', 'thumbnail', 'title')

    def get_courses_by_title(self, title: str):
        if title:
            return self.get_all_courses_queryset.filter(
                title__name__icontains=title,
                is_selling=True,
            )
        return Course.objects.none()

    def get_courses_by_list_id(self, list_id: list):
        if list_id:
            return self.get_all_courses_queryset.filter(id__in=list_id, is_selling=True)
        return Course.objects.none()


class CourseManagementService:
    def __init__(self, user):
        self.user = user

    @property
    def get_course_management_queryset(self):
        return CourseManagement.objects.prefetch_related(
            Prefetch("course__lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file"))),
                     ),
        ).select_related('course__topic', 'course__thumbnail').filter(user=self.user)

    @property
    def get_course_mngt_queryset_by_selling(self):
        query = Q(course__is_selling=True)
        query |= Q(course__is_selling=False) & Q(sale_status__in=[BOUGHT, PENDING])
        return self.get_course_management_queryset.filter(query).order_by('course__name')

    def get_courses_mngt_by_list_id(self, list_id: list):
        if list_id:
            return self.get_course_management_queryset.filter(course_id__in=list_id, course__is_selling=True)

    def calculate_course_progress(self, course_id):
        all_docs = CourseDocumentManagement.objects.filter(user=self.user, course_id=course_id, is_available=True)
        all_videos = VideoManagement.objects.filter(user=self.user, course_id=course_id, is_available=True)
        docs_completed = all_docs.filter(is_completed=True)
        videos_completed = all_videos.filter(is_completed=True)
        CourseManagement.objects.filter(user=self.user, course_id=course_id).update(
            progress=round(
                100 * (docs_completed.count() + videos_completed.count()) / (all_docs.count() + all_videos.count())
            )
        )

    def init_courses_management(self):
        if not CourseManagement.objects.filter(user=self.user).first():
            CourseManagement.objects.bulk_create([
                CourseManagement(
                    user=self.user, course=course, last_update=localtime()
                ) for course in CourseService().get_all_courses_queryset
            ])

    def custom_course_detail_data(self, data):
        """ Docs & videos completed """
        for count, lesson in enumerate(data['lessons'], start=0):
            lesson_mngt = LessonManagement.objects.filter(lesson_id=lesson['id']).first()
            if lesson_mngt:
                lesson_obj = lesson_mngt.lesson
                data['lessons'][count]['docs_completed'] = \
                    CourseDocumentManagement.objects.filter(
                        user=self.user,
                        course_id=data['id'],
                        document__in=lesson_obj.documents.all(),
                        is_completed=True,
                    ).values_list('document', flat=True)
                data['lessons'][count]['videos_completed'] = \
                    VideoManagement.objects.filter(
                        user=self.user,
                        course_id=data['id'],
                        video__in=lesson_obj.videos.all(),
                        is_completed=True,
                    ).values_list('video', flat=True)
            if not lesson_mngt:
                data['lessons'][count]['docs_completed'] = []
                data['lessons'][count]['videos_completed'] = []

        """ Rating """
        course_rating = CourseRating.objects.filter(course_id=data['id']).first()
        all_ratings = course_rating.ratings.all()
        my_rating = course_rating.ratings.filter(user=self.user).first()
        data['rating_detail'] = RatingSerializer(all_ratings, many=True).data if all_ratings else []
        data['my_rating'] = RatingSerializer(my_rating).data if my_rating else {}
        # Rating stats
        response = {}
        for score in range(1, 6):
            response["score_" + str(score)] = all_ratings.filter(rating=score).count()
        data['rating_stats'] = response

        """ Quiz detail """
        quiz_detail = {}
        quiz_answers = []
        correct_answers = 0
        total_answers = Answer.objects.filter(quiz__course_id=data['id'])
        for answer in total_answers:
            quiz_answers.append({
                "quiz_id": answer.quiz_id,
                "answer_choice": answer.choice,
                "correct_answer": answer.quiz.correct_answer.choice
            })
            if answer.choice == answer.quiz.correct_answer.choice:
                correct_answers += 1

        quiz_detail['correct_answers'] = correct_answers
        quiz_detail['total_quiz'] = len(total_answers)
        quiz_detail['quiz_answers'] = quiz_answers
        data['quiz_detail'] = quiz_detail

        return data

    def update_lesson_progress(self, course_id: str, lessons: list):
        documents_id = []
        videos_id = []
        for lesson in lessons:
            documents_id.extend(lesson["completed_docs"])
            videos_id.extend(lesson["completed_videos"])

        # set False only this course, set True for all course
        CourseDocumentManagement.objects.filter(user=self.user, course_id=course_id, is_available=True).update(is_completed=False)
        CourseDocumentManagement.objects.filter(user=self.user, document_id__in=documents_id, is_available=True).update(is_completed=True)
        VideoManagement.objects.filter(user=self.user, course_id=course_id, is_available=True).update(is_completed=False)
        VideoManagement.objects.filter(user=self.user, video_id__in=videos_id, is_available=True).update(is_completed=True)

        self.calculate_course_progress(course_id)


class UserDataManagementService:
    def __init__(self, user):
        self.user = user

    def init_user_data(self):
        if not CourseManagement.objects.filter(user=self.user).first():
            CourseManagement.objects.bulk_create([
                CourseManagement(user=self.user, course=course, last_update=localtime())
                for course in CourseService(self.user).get_all_courses_queryset
            ])
