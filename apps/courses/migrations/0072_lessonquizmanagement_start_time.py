# Generated by Django 4.0.5 on 2023-10-03 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0071_remove_lessonmanagement_date_done_quiz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonquizmanagement',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]