# Generated by Django 4.0.5 on 2023-11-28 18:14

from django.db import migrations, models
import django.utils.timezone
import django_better_admin_arrayfield.models.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_user_quiz_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('permissions', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Permission Groups',
            },
        ),
    ]
