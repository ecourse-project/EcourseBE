import uuid

from apps.rating.enums import RATE_CHOICES
from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.documents.models import Document
from apps.courses.models import Course


class Rating(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    rating = models.SmallIntegerField(choices=RATE_CHOICES, null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.rating}"

    class Meta:
        ordering = ['-created']


class DocumentRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(Document, related_name='ratings', on_delete=models.CASCADE)
    rating = models.ManyToManyField(Rating, blank=True)

    def __str__(self):
        return self.document.name


class CourseRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.OneToOneField(Course, related_name='ratings', on_delete=models.CASCADE)
    rating = models.ManyToManyField(Rating, blank=True)

    def __str__(self):
        return self.course.name
