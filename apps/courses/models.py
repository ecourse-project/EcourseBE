import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.courses.enums import PROGRESS_STATUS, IN_PROGRESS, SALE_STATUSES, AVAILABLE
from apps.upload.models import UploadImage, UploadFile, UploadVideo


class CourseTopic(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CourseDocument(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey(CourseTopic, related_name="course_docs", on_delete=models.SET_NULL, null=True, blank=True)
    file = models.ForeignKey(UploadFile, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Lesson(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    videos = models.ManyToManyField(UploadVideo, blank=True)
    documents = models.ManyToManyField(CourseDocument, blank=True)
    lesson_number = models.SmallIntegerField(default=1, null=True, blank=True, verbose_name="order")
    total_documents = models.PositiveSmallIntegerField(default=0)
    total_videos = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["lesson_number"]

    def __str__(self):
        return self.name

    @property
    def total_docs_videos(self):
        return self.total_videos + self.total_documents


class Course(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(CourseTopic, related_name="courses", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    lessons = models.ManyToManyField(Lesson, blank=True, related_name="courses")
    thumbnail = models.ForeignKey(
        UploadImage, related_name="courses", on_delete=models.SET_NULL, null=True, blank=True,
    )
    views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_selling = models.BooleanField(default=True)
    course_of_class = models.BooleanField(default=False)
    num_of_rates = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CourseManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_mngt", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    progress = models.SmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PROGRESS_STATUS, default=IN_PROGRESS)
    mark = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    is_done_quiz = models.BooleanField(default=False)
    date_done_quiz = models.DateTimeField(null=True, blank=True)
    sale_status = models.CharField(max_length=15, choices=SALE_STATUSES, default=AVAILABLE)
    is_favorite = models.BooleanField(default=False)
    user_in_class = models.BooleanField(null=True)
    init_data = models.BooleanField(default=False)

    class Meta:
        ordering = ["course__name"]
        verbose_name_plural = "Management - Courses"
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.course.name} - {self.user.__str__()}"


class LessonQuizManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_mngt = models.ForeignKey(CourseManagement, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_done_quiz = models.BooleanField(default=False)
    date_done_quiz = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.course_mngt.course.name} - {self.course_mngt.user.__str__()}"


class LessonManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_mngt", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(id)

    class Meta:
        unique_together = ('lesson', 'course')
        verbose_name_plural = "Management - Lessons"


class CourseDocumentManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        CourseDocument, on_delete=models.CASCADE, related_name="course_doc_mngt", null=True, blank=True
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_doc_mngt", null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(id)

    class Meta:
        unique_together = ('document', 'lesson', 'course', 'user')
        verbose_name_plural = "Management - Course's Documents"


class VideoManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="video_mngt", null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_mngt", null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('video', 'lesson', 'course', 'user')
        verbose_name_plural = "Management - Videos"
