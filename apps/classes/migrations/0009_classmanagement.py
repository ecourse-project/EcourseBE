# Generated by Django 4.0.5 on 2023-04-01 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0057_course_course_of_class_and_more'),
        ('classes', '0008_alter_classtopic_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassManagement',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('courses.coursemanagement',),
        ),
    ]
