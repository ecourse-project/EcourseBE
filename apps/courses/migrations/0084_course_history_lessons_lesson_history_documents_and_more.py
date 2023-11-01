# Generated by Django 4.0.5 on 2023-10-31 21:05

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0083_coursemanagement_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='history_lessons',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='lesson',
            name='history_documents',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='lesson',
            name='history_videos',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
    ]
