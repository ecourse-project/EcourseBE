# Generated by Django 4.0.5 on 2022-09-17 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0022_remove_document_users_documentmanagement'),
        ('upload', '0004_remove_uploadfile_user_remove_uploadimage_user'),
        ('courses', '0004_remove_course_is_activated_remove_lesson_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='document',
            field=models.ManyToManyField(blank=True, to='documents.document'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=models.ManyToManyField(blank=True, to='upload.uploadfile'),
        ),
    ]
