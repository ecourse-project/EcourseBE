# Generated by Django 4.0.5 on 2024-01-06 14:27

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_systemconfig_data_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitStatistics',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visit', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]