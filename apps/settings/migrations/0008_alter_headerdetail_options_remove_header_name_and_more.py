# Generated by Django 4.0.5 on 2023-03-21 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0055_alter_coursetopic_name'),
        ('documents', '0040_alter_documenttopic_options'),
        ('classes', '0008_alter_classtopic_options'),
        ('posts', '0001_initial'),
        ('settings', '0007_alter_homepagedetail_options_homepagedetail_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='headerdetail',
            options={'ordering': ['header', 'order']},
        ),
        migrations.RemoveField(
            model_name='header',
            name='name',
        ),
        migrations.AddField(
            model_name='headerdetail',
            name='class_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.classtopic'),
        ),
        migrations.AddField(
            model_name='headerdetail',
            name='post_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.posttopic'),
        ),
        migrations.AlterField(
            model_name='headerdetail',
            name='course_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.coursetopic'),
        ),
        migrations.AlterField(
            model_name='headerdetail',
            name='document_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.documenttopic'),
        ),
        migrations.AlterField(
            model_name='headerdetail',
            name='header',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='header_detail', to='settings.header'),
        ),
    ]
