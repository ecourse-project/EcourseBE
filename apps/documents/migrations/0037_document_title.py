# Generated by Django 4.0.5 on 2023-01-10 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0036_documenttitle_remove_document_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='docs', to='documents.documenttitle'),
        ),
    ]
