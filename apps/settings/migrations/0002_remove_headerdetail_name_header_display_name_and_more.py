# Generated by Django 4.0.5 on 2023-01-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='headerdetail',
            name='name',
        ),
        migrations.AddField(
            model_name='header',
            name='display_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='headerdetail',
            name='display_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='header',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
