# Generated by Django 4.0.5 on 2023-05-23 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0020_alter_uploadfile_file_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='ip_address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='ip_address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='uploadvideo',
            name='ip_address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
