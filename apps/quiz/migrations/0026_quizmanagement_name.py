# Generated by Django 4.0.5 on 2023-10-24 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0025_alter_matchcolumnmatchanswer_first_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmanagement',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
