# Generated by Django 4.0.5 on 2023-01-10 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0050_coursetitle_course_title'),
        ('settings', '0002_remove_headerdetail_name_header_display_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='headerdetail',
            name='course_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.coursetitle'),
        ),
    ]
