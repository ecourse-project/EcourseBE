# Generated by Django 4.0.5 on 2023-10-09 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0026_uploadfolder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadCourse',
        ),
        migrations.DeleteModel(
            name='UploadDocument',
        ),
    ]