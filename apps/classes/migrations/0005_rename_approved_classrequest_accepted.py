# Generated by Django 4.0.5 on 2023-03-20 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_alter_class_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classrequest',
            old_name='approved',
            new_name='accepted',
        ),
    ]
