# Generated by Django 4.0.5 on 2023-09-23 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0024_alter_uploadfile_file_embedded_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadAvatar',
            fields=[
            ],
            options={
                'verbose_name_plural': 'User Avatar',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('upload.uploadimage',),
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='is_avatar',
            field=models.BooleanField(default=False),
        ),
    ]
