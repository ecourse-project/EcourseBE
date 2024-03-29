# Generated by Django 4.0.5 on 2023-05-16 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0019_calculate_file_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file_path',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='uploadimage',
            name='image_path',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='uploadvideo',
            name='video_path',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]
