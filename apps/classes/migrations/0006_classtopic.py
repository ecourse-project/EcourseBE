# Generated by Django 4.0.5 on 2023-03-20 09:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0005_rename_approved_classrequest_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTopic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
