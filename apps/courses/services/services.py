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
from apps.quiz.models import Answer
from apps.classes.services.services import ClassRequestService


class CourseService:
    @property
    def get_all_courses_queryset(self):
        return Course.objects.prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.prefetch_related(
                Prefetch("videos"),
                Prefetch("documents", queryset=CourseDocument.objects.select_related("file")))
                     )
        ).select_related('topic', 'thumbnail').filter(course_of_class=False)

    def get_courses_by_topic(self, topic: str):
        if topic.strip():
            return self.get_all_courses_queryset.filter(
                topic__name__icontains=topic.strip(),
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
        ).select_related('course__topic', 'course__thumbnail').filter(user=self.user, course__course_of_class=False)

    @property
    def get_course_mngt_queryset_by_selling(self):
        query = Q(course__is_selling=True)
        query |= Q(course__is_selling=False) & Q(sale_status__in=[BOUGHT, PENDING])
        return self.get_course_management_queryset.filter(query).order_by('course__name')

    def get_courses_mngt_by_list_id(self, list_id: list):
        if list_id:
            return self.get_course_mngt_queryset_by_selling.filter(course_id__in=list_id)

    def calculate_course_progress(self, course_id):
        progress = 0
        all_docs = CourseDocumentManagement.objects.filter(user=self.user, course_id=course_id, is_available=True)
        all_videos = VideoManagement.objects.filter(user=self.user, course_id=course_id, is_available=True)
        if all_videos.exists() or all_docs.exists():
            docs_completed = all_docs.filter(is_completed=True)
            videos_completed = all_videos.filter(is_completed=True)
            progress = round(
                100 * (docs_completed.count() + videos_completed.count()) / (all_docs.count() + all_videos.count())
            )
        CourseManagement.objects.filter(user=self.user, course_id=course_id).update(progress=progress)
        return progress

    def init_courses_management(self):
        if not CourseManagement.objects.filter(user=self.user).first():
            CourseManagement.objects.bulk_create([
                CourseManagement(
                    user=self.user, course=course, last_update=localtime()
                ) for course in CourseService().get_all_courses_queryset
            ])

    def custom_course_detail_data(self, data, instance=None):
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
                        is_available=True,
                    ).values_list('document', flat=True)
                data['lessons'][count]['videos_completed'] = \
                    VideoManagement.objects.filter(
                        user=self.user,
                        course_id=data['id'],
                        video__in=lesson_obj.videos.all(),
                        is_completed=True,
                        is_available=True,
                    ).values_list('video', flat=True)
            else:
                data['lessons'][count]['docs_completed'] = []
                data['lessons'][count]['videos_completed'] = []

        """ Rating """
        # course_rating = CourseRating.objects.filter(course_id=data['id']).first()
        # all_ratings = course_rating.ratings.all()
        # my_rating = course_rating.ratings.filter(user=self.user).first()
        # data['rating_detail'] = RatingSerializer(all_ratings, many=True).data if all_ratings else []
        # data['my_rating'] = RatingSerializer(my_rating).data if my_rating else {}
        # Rating stats
        # response = {}
        # for score in range(1, 6):
        #     response["score_" + str(score)] = all_ratings.filter(rating=score).count()
        # data['rating_stats'] = response

        """ Quiz detail """
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

        quiz_detail['correct_answers'] = correct_answers
        quiz_detail['total_quiz'] = len(total_answers)
        quiz_detail['quiz_answers'] = quiz_answers
        data['quiz_detail'] = quiz_detail

        if not data.get("request_status"):
            data["request_status"] = None
            if data.get("course_of_class") and instance:
                data["request_status"] = ClassRequestService().get_user_request_status(
                    user=self.user,
                    class_obj=instance.course,
                )

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

        return self.calculate_course_progress(course_id)
