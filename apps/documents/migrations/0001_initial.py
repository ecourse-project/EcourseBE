# Generated by Django 4.0.5 on 2022-08-01 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_activated', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('files', models.ManyToManyField(blank=True, null=True, related_name='documents', to='upload.uploadfile')),
                ('thumbnail', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document', to='upload.uploadfile')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
