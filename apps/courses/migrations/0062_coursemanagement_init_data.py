# Generated by Django 4.0.5 on 2023-05-28 06:50

from django.db import migrations, models
from apps.courses.enums import BOUGHT


def update_init_data(apps, schema_editor):
    CourseManagement = apps.get_model("courses", "CourseManagement")

    list_objs = []
    for obj in CourseManagement.objects.all():
        if obj.user_in_class or obj.sale_status == BOUGHT:
            obj.init_data = True
            list_objs.append(obj)

    CourseManagement.objects.bulk_update(list_objs, fields=["init_data"])


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0061_alter_lesson_videos_alter_videomanagement_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemanagement',
            name='init_data',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(update_init_data)
    ]