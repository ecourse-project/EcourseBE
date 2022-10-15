# Generated by Django 4.0.5 on 2022-10-08 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_remove_uploadfile_user_remove_uploadimage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='duration',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='uploadfile',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]