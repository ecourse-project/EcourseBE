# Generated by Django 4.0.5 on 2023-03-20 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0008_alter_uploadfile_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadfile',
            options={'ordering': ['file_name']},
        ),
        migrations.AlterModelOptions(
            name='uploadimage',
            options={'ordering': ['image_name']},
        ),
    ]