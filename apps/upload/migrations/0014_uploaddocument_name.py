# Generated by Django 4.0.5 on 2023-04-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0013_uploadcourse_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaddocument',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
