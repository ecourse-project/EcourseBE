# Generated by Django 4.0.5 on 2022-09-19 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_rename_lesson_course_lessons_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['name']},
        ),
    ]
