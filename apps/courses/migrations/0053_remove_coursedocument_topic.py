# Generated by Django 4.0.5 on 2023-03-17 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0052_delete_coursetitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedocument',
            name='topic',
        ),
    ]
