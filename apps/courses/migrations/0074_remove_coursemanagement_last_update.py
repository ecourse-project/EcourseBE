# Generated by Django 4.0.5 on 2023-10-09 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0073_alter_coursemanagement_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursemanagement',
            name='last_update',
        ),
    ]
