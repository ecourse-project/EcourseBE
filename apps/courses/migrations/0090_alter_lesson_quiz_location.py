# Generated by Django 4.0.5 on 2023-11-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0089_course_author_coursedocument_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='quiz_location',
            field=models.JSONField(blank=True, default={}, null=True),
        ),
    ]
