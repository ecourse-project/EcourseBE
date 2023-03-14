from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.rating.models import DocumentRating, CourseRating


def update_document_rating(document, rating):
    if rating is not None:
        document.rating = (document.rating * document.num_of_rates + rating) / (document.num_of_rates + 1)
        document.num_of_rates += 1
        document.save(update_fields=["num_of_rates", "rating"])


def update_course_rating(course, rating):
    if rating is not None:
        course.rating = (course.rating * course.num_of_rates + rating) / (course.num_of_rates + 1)
        course.num_of_rates += 1
        course.save(update_fields=["num_of_rates", "rating"])


@receiver(m2m_changed, sender=DocumentRating.ratings.through)
def update_document_rating_signal(sender, instance: DocumentRating, action, model, pk_set, **kwargs):
    if action == "post_add":
        rating_pk = list(pk_set)[0]
        rating_obj = model.objects.get(pk=rating_pk)
        update_document_rating(instance.document, rating_obj.rating)


@receiver(m2m_changed, sender=CourseRating.ratings.through)
def update_course_rating_signal(sender, instance: CourseRating, action, model, pk_set, **kwargs):
    if action == "post_add":
        rating_pk = list(pk_set)[0]
        rating_obj = model.objects.get(pk=rating_pk)
        update_course_rating(instance.course, rating_obj.rating)
