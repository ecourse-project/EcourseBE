# Generated by Django 4.0.5 on 2022-10-22 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0041_lessonmanagement_course'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessonmanagement',
            unique_together=set(),
        ),
    ]