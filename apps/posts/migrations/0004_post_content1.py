# Generated by Django 4.0.5 on 2023-05-14 02:47

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content1',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
