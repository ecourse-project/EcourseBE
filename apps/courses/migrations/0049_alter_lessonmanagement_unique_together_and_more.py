# Generated by Django 4.0.5 on 2022-10-25 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0048_alter_coursedocumentmanagement_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessonmanagement',
            unique_together={('lesson', 'course')},
        ),
        migrations.RemoveField(
            model_name='lessonmanagement',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='lessonmanagement',
            name='user',
        ),
    ]