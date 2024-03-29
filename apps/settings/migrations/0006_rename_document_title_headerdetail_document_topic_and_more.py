# Generated by Django 4.0.5 on 2023-03-16 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0051_rename_topic_coursetopic_and_more'),
        ('settings', '0005_alter_homepagedetail_courses_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='headerdetail',
            old_name='document_title',
            new_name='document_topic',
        ),
        migrations.RemoveField(
            model_name='headerdetail',
            name='course_title',
        ),
        migrations.AddField(
            model_name='headerdetail',
            name='course_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.coursetopic'),
        ),
    ]
