# Generated by Django 4.0.5 on 2023-05-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_options_post_content_summary_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
