# Generated by Django 4.0.5 on 2023-10-05 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_alter_userdatabackup_classes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdatabackup',
            name='classes',
        ),
    ]