# Generated by Django 4.0.5 on 2023-03-21 09:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('document_time_limit', models.PositiveSmallIntegerField(blank=True, help_text='(hours)', null=True)),
            ],
        ),
    ]
