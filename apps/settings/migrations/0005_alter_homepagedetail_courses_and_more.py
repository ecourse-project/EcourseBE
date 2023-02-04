# Generated by Django 4.0.5 on 2023-01-14 12:02

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0004_homepagedetail_headerdetail_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagedetail',
            name='courses',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='homepagedetail',
            name='documents',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
    ]