# Generated by Django 4.0.5 on 2022-10-21 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_remove_answer_course_answer_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='question_number',
        ),
    ]