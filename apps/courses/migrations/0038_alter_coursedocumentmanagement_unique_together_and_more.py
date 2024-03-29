# Generated by Django 4.0.5 on 2022-10-21 19:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_uploadfile_duration_uploadfile_file_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0037_remove_lessonmanagement_docs_completed_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursedocumentmanagement',
            unique_together={('document', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='lessonmanagement',
            unique_together={('lesson', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='videomanagement',
            unique_together={('video', 'user')},
        ),
    ]
