# Generated by Django 4.0.5 on 2023-03-21 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0007_class_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classtopic',
            options={'ordering': ['name']},
        ),
    ]