# Generated by Django 4.0.5 on 2023-11-09 01:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0033_alter_quiz_options_remove_quiz_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
