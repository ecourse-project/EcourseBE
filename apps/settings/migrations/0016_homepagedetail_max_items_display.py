# Generated by Django 4.0.5 on 2023-10-26 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0015_alter_homepagedetail_options_homepagedetail_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagedetail',
            name='max_items_display',
            field=models.PositiveSmallIntegerField(default=6),
        ),
    ]
