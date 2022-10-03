from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Sum

from apps.carts.models import Cart


def calculate_total_price(cart):
    docs_price = Cart.objects.aggregate(total_price=Sum('documents__price'))['total_price']
    courses_price = Cart.objects.aggregate(total_price=Sum('courses__price'))['total_price']
    if not docs_price:
        docs_price = 0
    if not courses_price:
        courses_price = 0
    cart.total_price = docs_price + courses_price
    cart.save(update_fields=['total_price'])


@receiver(m2m_changed, sender=Cart.documents.through)
def update_cart_total_price_signal(sender, instance: Cart, action, model, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove":
        calculate_total_price(instance)


@receiver(m2m_changed, sender=Cart.courses.through)
def update_cart_total_price_signal(sender, instance: Cart, action, model, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove":
        calculate_total_price(instance)
