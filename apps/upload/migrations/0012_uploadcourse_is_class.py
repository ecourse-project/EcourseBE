# Generated by Django 4.0.5 on 2023-04-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0011_uploaddocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadcourse',
            name='is_class',
            field=models.BooleanField(default=False),
        ),
    ]