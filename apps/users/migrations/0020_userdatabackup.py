# Generated by Django 4.0.5 on 2023-10-05 09:12

from django.db import migrations, models
import django.utils.timezone
import django_better_admin_arrayfield.models.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDataBackUp',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documents', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('courses', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
