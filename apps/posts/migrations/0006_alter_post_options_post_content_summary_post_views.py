# Generated by Django 4.0.5 on 2023-05-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_post_content1_alter_post_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['views']},
        ),
        migrations.AddField(
            model_name='post',
            name='content_summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
