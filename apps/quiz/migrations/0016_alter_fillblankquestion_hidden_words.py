# Generated by Django 4.0.5 on 2023-09-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_alter_fillblankquestion_hidden_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fillblankquestion',
            name='hidden_words',
            field=models.JSONField(blank=True, null=True),
        ),
    ]