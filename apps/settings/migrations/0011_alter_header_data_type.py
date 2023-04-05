# Generated by Django 4.0.5 on 2023-03-31 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0010_header_data_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='header',
            name='data_type',
            field=models.CharField(blank=True, choices=[('DOCUMENT', 'DOCUMENT'), ('COURSE', 'COURSE'), ('CLASS', 'CLASS'), ('POST', 'POST')], max_length=20, null=True),
        ),
    ]