# Generated by Django 4.0.5 on 2023-05-19 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_personalinfo_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalinfo',
            name='name',
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='payment_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]