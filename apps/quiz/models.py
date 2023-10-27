import uuid

from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.courses.models import Course, Lesson
from apps.quiz import enums
from apps.upload.models import UploadImage
from apps.core.utils import get_summary_content


# =====================================================Choices quiz=====================================================
class ChoicesQuizChoiceName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Choices quiz - Choice name"
        verbose_name = "Choice"


class ChoicesQuizAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer_type = models.CharField(max_length=20, choices=enums.ANSWER_TYPES, default=enums.ANSWER_TYPE_TEXT)
    answer_text = models.TextField(null=True, blank=True)
    answer_image = models.ForeignKey(UploadImage, on_delete=models.SET_NULL, null=True, blank=True)
    choice_name = models.ForeignKey(ChoicesQuizChoiceName, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        answer = f"{enums.ANSWER_TYPE_TEXT} - {get_summary_content(self.answer_text or 'None', 9)}"
        if self.answer_type == enums.ANSWER_TYPE_IMAGE:
            answer = f"{enums.ANSWER_TYPE_IMAGE} - {get_summary_content(self.answer_image.image_name if self.answer_image else 'None', 9)}"
        return f"{self.choice_name or 'None'} - {answer}"

    class Meta:
        ordering = ["choice_name__name"]
        verbose_name_plural = "Choices quiz - Answers"
        verbose_name = "Answer"


class ChoicesQuizQuestion(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_text = models.TextField(null=True, blank=True)
    content_image = models.ForeignKey(UploadImage, on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.CharField(max_length=20, choices=enums.ANSWER_TYPES, default=enums.ANSWER_TYPE_TEXT)
    choices = models.ManyToManyField(ChoicesQuizAnswer, blank=True)
    correct_answer = models.ForeignKey(ChoicesQuizChoiceName, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        content = f"{enums.ANSWER_TYPE_TEXT} - {get_summary_content(self.content_text or 'None', 9)}"
        if self.content_type == enums.ANSWER_TYPE_IMAGE:
            content = f"{enums.ANSWER_TYPE_IMAGE} - {get_summary_content(self.content_image.image_name if self.content_image else 'None', 9)}"
        return content

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "Choices quiz - Questions"
        verbose_name = "Question"


# =====================================================Match Column=====================================================
class MatchColumnContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(max_length=20, choices=enums.ANSWER_TYPES, default=enums.ANSWER_TYPE_TEXT)
    content_text = models.TextField(null=True, blank=True)
    content_image = models.ForeignKey(UploadImage, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        content = f"{enums.ANSWER_TYPE_TEXT} - {get_summary_content(self.content_text or 'None', 9)}"
        if self.content_type == enums.ANSWER_TYPE_IMAGE:
            content = f"{enums.ANSWER_TYPE_IMAGE} - {get_summary_content(self.content_image.image_name if self.content_image else 'None', 9)}"
        return content

    class Meta:
        ordering = ["content_type", "content_text"]
        verbose_name_plural = "Match column - Content"
        verbose_name = "Content"


class MatchColumnMatchAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match_question = models.ForeignKey("MatchColumnQuestion", on_delete=models.CASCADE, null=True, blank=True)
    first_content = models.ForeignKey(MatchColumnContent, on_delete=models.CASCADE, null=True, blank=True, related_name="match_answer_from_first")
    second_content = models.ForeignKey(MatchColumnContent, on_delete=models.CASCADE, null=True, blank=True, related_name="match_answer_from_second")

    def __str__(self):
        first = second = 'None'
        if self.first_content:
            content_type = self.first_content.content_type
            first = (
                get_summary_content(self.first_content.content_text)
                if content_type == enums.ANSWER_TYPE_TEXT
                else get_summary_content(self.first_content.content_image.image_name)
            )
        if self.second_content:
            content_type = self.second_content.content_type
            second = (
                get_summary_content(self.second_content.content_text)
                if content_type == enums.ANSWER_TYPE_TEXT
                else get_summary_content(self.second_content.content_image.image_name)
            )

        return f"{first} - {second}"

    class Meta:
        verbose_name_plural = "Match column - Match answer"
        verbose_name = "Answer"


class MatchColumnQuestion(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=True, blank=True)
    first_column = models.ManyToManyField(MatchColumnContent, related_name="questions_from_first_col")
    second_column = models.ManyToManyField(MatchColumnContent, related_name="questions_from_second_col")

    def __str__(self):
        return get_summary_content(self.content or 'None', 10)

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "Match column - Questions"
        verbose_name = "Question"


# ======================================================Fill Blank======================================================
class FillBlankQuestion(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=True, blank=True)
    hidden_words = models.JSONField(null=True, blank=True)

    def __str__(self):
        return get_summary_content(self.content or 'None', 10)

    class Meta:
        verbose_name_plural = "Fill blank - Questions"
        verbose_name = "Question"


# ======================================================Management======================================================
class QuizManagement(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=1)
    question_type = models.CharField(max_length=20, choices=enums.QUESTION_TYPES, null=True, blank=True)
    choices_question = models.ForeignKey(ChoicesQuizQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    match_question = models.ForeignKey(MatchColumnQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    fill_blank_question = models.ForeignKey(FillBlankQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    time_limit = models.PositiveSmallIntegerField(null=True, blank=True, help_text="(seconds)")

    def __str__(self):
        return f"{self.order} - {self.course.name if self.course else 'None'}"

    class Meta:
        ordering = ["course", "order"]
        verbose_name_plural = "Management"
        verbose_name = "Quiz"


# =======================================================Answers========================================================
class MatchColumnUserAnswer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizManagement, on_delete=models.CASCADE)
    first_content = models.ForeignKey(MatchColumnContent, on_delete=models.SET_NULL, null=True, blank=True, related_name="match_user_answer_from_first")
    second_content = models.ForeignKey(MatchColumnContent, on_delete=models.SET_NULL, null=True, blank=True, related_name="match_user_answer_from_second")

    def __str__(self):
        course_name = self.quiz.course.name if self.quiz and self.quiz.course else "None"
        return f"{self.user.full_name} - {get_summary_content(course_name)}"

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "Match column - User answers"
        verbose_name = "Answer"


class ChoicesQuizUserAnswer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizManagement, on_delete=models.CASCADE)
    choice = models.ForeignKey(ChoicesQuizChoiceName, on_delete=models.SET_NULL, null=True, blank=True, help_text="(Choices quiz answer)")

    def __str__(self):
        course_name = self.quiz.course.name if self.quiz and self.quiz.course else "None"
        return f"{self.user.full_name} - {get_summary_content(course_name)}"

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "Choices quiz - User answers"
        verbose_name = "Answer"


class FillBlankUserAnswer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizManagement, on_delete=models.CASCADE)
    words = ArrayField(models.CharField(max_length=100), null=True, blank=True)

    def __str__(self):
        course_name = self.quiz.course.name if self.quiz and self.quiz.course else "None"
        return f"{self.user.full_name} - {get_summary_content(course_name)}"

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "Fill blank - User answers"
        verbose_name = "Answer"