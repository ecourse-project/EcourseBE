# Generated by Django 4.0.5 on 2022-09-21 08:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_remove_uploadfile_user_remove_uploadimage_user'),
        ('courses', '0013_alter_course_options_alter_lesson_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDocument',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='upload.uploadfile')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='lesson',
            name='documents',
            field=models.ManyToManyField(blank=True, to='courses.coursedocument'),
        ),
    ]
