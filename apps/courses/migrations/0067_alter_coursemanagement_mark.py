# Generated by Django 4.0.5 on 2023-09-30 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0066_alter_coursedocument_options_coursedocument_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemanagement',
            name='mark',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
