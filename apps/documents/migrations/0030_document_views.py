# Generated by Django 4.0.5 on 2022-09-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0029_documentmanagement_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
