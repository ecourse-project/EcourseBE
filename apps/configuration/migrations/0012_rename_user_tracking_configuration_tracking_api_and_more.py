# Generated by Django 4.0.5 on 2023-11-02 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0011_configuration_use_celery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='user_tracking',
            new_name='tracking_api',
        ),
        migrations.AddField(
            model_name='configuration',
            name='tracking_device',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='tracking_ip',
            field=models.BooleanField(default=False),
        ),
    ]
