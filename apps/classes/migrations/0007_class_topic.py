# Generated by Django 4.0.5 on 2023-03-20 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_classtopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.classtopic'),
        ),
    ]