# Generated by Django 4.0.5 on 2022-09-23 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0026_alter_document_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentmanagement',
            options={'ordering': ['document__name']},
        ),
    ]
