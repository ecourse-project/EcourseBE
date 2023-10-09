# Generated by Django 4.0.5 on 2023-10-05 09:20

from django.db import migrations, models


def update_order_code(apps, schema_editor):
    Order = apps.get_model("payment", "Order")

    list_orders = []
    for order in Order.objects.all():
        order.code = order.code.split("-")[0]
        list_orders.append(order)

    Order.objects.bulk_update(list_orders, fields=["code"])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_userdatabackup_classes_userdatabackup_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdatabackup',
            name='classes',
        ),
        migrations.RemoveField(
            model_name='userdatabackup',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='userdatabackup',
            name='documents',
        ),
        migrations.AddField(
            model_name='userdatabackup',
            name='classes',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userdatabackup',
            name='courses',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userdatabackup',
            name='documents',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
