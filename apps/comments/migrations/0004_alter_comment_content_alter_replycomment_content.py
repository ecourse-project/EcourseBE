# Generated by Django 4.0.5 on 2023-09-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_replycomment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='replycomment',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]