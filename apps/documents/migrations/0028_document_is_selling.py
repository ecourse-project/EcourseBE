# Generated by Django 4.0.5 on 2022-09-23 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0027_alter_documentmanagement_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_selling',
            field=models.BooleanField(default=True),
        ),
    ]
