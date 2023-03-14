# Generated by Django 4.0.5 on 2022-10-15 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0029_remove_coursemanagement_docs_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemanagement',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_mngt', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='lessonmanagement',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_mngt', to='courses.lesson'),
        ),
    ]
