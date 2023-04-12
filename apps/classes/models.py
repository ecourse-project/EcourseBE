import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.courses.models import Course, CourseManagement
from apps.users.models import User


# class ClassTopic(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, null=True, blank=True)
#
#     class Meta:
#         ordering = ["name"]
#
#     def __str__(self):
#         return self.name


# class Class(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
#     topic = models.ForeignKey(ClassTopic, on_delete=models.SET_NULL, null=True, blank=True)
#     users = models.ManyToManyField(User, blank=True, related_name="user_classes")
#
#     class Meta:
#         verbose_name = "class"
#         verbose_name_plural = "classes"
#
#     def __str__(self):
#         return self.name


class Class(Course):
    class Meta:
        proxy = True
        verbose_name = "class"
        verbose_name_plural = "classes"


class ClassRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_request = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_request = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["class_request__name"]


class ClassManagement(CourseManagement):
    class Meta:
        proxy = True
        verbose_name_plural = "Management - Classes"
