# Generated by Django 4.0.5 on 2023-03-20 06:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='users',
            field=models.ManyToManyField(related_name='user_classes', to=settings.AUTH_USER_MODEL),
        ),
    ]