# Generated by Django 4.0.5 on 2022-10-16 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0031_lessonmanagement_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonmanagement',
            name='progress',
        ),
    ]
