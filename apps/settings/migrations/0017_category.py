# Generated by Django 4.0.5 on 2023-12-05 22:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0016_homepagedetail_max_items_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
    ]
