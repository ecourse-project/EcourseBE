# Generated by Django 4.0.5 on 2023-11-02 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0086_course_structure'),
        ('quiz', '0028_alter_quizmanagement_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.lesson'),
        ),
    ]
