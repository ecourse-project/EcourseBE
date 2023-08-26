import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.users.models import User
from apps.documents.models import Document
from apps.courses.models import Course
from apps.payment.enums import STATUSES, PENDING


class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name='orders', on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    documents = models.ManyToManyField(Document, blank=True, related_name='orders')
    courses = models.ManyToManyField(Course, blank=True, related_name='orders')
    status = models.CharField(max_length=8, choices=STATUSES, default=PENDING)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        ordering = ["-created"]
