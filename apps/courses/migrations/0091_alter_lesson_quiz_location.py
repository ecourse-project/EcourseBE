# Generated by Django 4.0.5 on 2023-11-24 11:47

from django.db import migrations, models


def update_quiz_location(apps, schema_editor):
    Lesson = apps.get_model("courses", "Lesson")
    Lesson.objects.all().update(quiz_location=None)


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0090_alter_lesson_quiz_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='quiz_location',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.RunPython(update_quiz_location),
    ]
