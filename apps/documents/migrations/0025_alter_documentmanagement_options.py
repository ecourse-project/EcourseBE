# Generated by Django 4.0.5 on 2022-09-20 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0024_alter_document_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentmanagement',
            options={'ordering': ['-document__sold']},
        ),
    ]
