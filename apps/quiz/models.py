import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.courses.models import Course
from apps.quiz.enums import ANSWER_CHOICES


class AnswerChoices(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice = models.CharField(max_length=5, choices=ANSWER_CHOICES)

    def __str__(self):
        return self.choice


class Quiz(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=200)
    A = models.CharField(max_length=255)
    B = models.CharField(max_length=255)
    C = models.CharField(max_length=255)
    D = models.CharField(max_length=255)
    correct_answer = models.ForeignKey(AnswerChoices, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question


class Answer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice = models.CharField(max_length=5, choices=ANSWER_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.choice


