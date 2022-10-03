import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.documents.models import Document
from apps.courses.models import Course


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0)
    documents = models.ManyToManyField(Document, blank=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.user.full_name


class FavoriteList(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="favorite_list", null=True, blank=True)
    documents = models.ManyToManyField(Document, blank=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.user.full_name

