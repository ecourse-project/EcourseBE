# Generated by Django 4.0.5 on 2023-11-04 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0032_alter_choicesquestionuseranswer_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['name'], 'verbose_name': 'Quiz', 'verbose_name_plural': 'Quiz'},
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='lesson',
        ),
    ]