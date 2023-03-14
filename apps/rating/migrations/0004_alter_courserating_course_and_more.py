# Generated by Django 4.0.5 on 2022-10-18 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0033_remove_lessonmanagement_status_and_more'),
        ('documents', '0035_alter_documentmanagement_document'),
        ('rating', '0003_alter_rating_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courserating',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='documentrating',
            name='document',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='documents.document'),
        ),
    ]
