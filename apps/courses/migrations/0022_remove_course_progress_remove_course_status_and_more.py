# Generated by Django 4.0.5 on 2022-09-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_alter_coursemanagement_sale_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='course',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='progress',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='status',
        ),
        migrations.AddField(
            model_name='coursemanagement',
            name='is_done_quiz',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coursemanagement',
            name='mark',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='coursemanagement',
            name='progress',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='coursemanagement',
            name='status',
            field=models.CharField(choices=[('IN_PROGRESS', 'IN_PROGRESS'), ('DONE', 'DONE')], default='IN_PROGRESS', max_length=20),
        ),
    ]
