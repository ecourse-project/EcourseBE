# Generated by Django 4.0.5 on 2023-03-07 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_userresetpassword_password_reset'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresetpassword',
            name='is_changed',
            field=models.BooleanField(default=True),
        ),
    ]
