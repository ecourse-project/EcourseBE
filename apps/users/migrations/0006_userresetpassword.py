# Generated by Django 4.0.5 on 2023-02-15 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserResetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('password_reset', models.CharField(max_length=1000)),
            ],
        ),
    ]
