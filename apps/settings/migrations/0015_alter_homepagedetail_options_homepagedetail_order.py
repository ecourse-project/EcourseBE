# Generated by Django 4.0.5 on 2023-08-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0014_rename_course_topic_headerdetail_course_and_class_topic_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepagedetail',
            options={'ordering': ['order', 'display_name']},
        ),
        migrations.AddField(
            model_name='homepagedetail',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]