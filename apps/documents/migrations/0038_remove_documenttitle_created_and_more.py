# Generated by Django 4.0.5 on 2023-01-10 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0037_document_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documenttitle',
            name='created',
        ),
        migrations.RemoveField(
            model_name='documenttitle',
            name='modified',
        ),
    ]
