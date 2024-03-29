# Generated by Django 4.0.5 on 2023-05-18 15:41

from django.db import migrations, models
import django.db.models.deletion


def sync_post_header(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    Header = apps.get_model("settings", "Header")

    list_posts = []
    for post in Post.objects.all():
        if post.header:
            header = Header.objects.filter(display_name__iexact=post.header).first()
            post.header_fk = header if header else None
            list_posts.append(post)

    Post.objects.bulk_update(list_posts, fields=["header_fk"])


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0014_rename_course_topic_headerdetail_course_and_class_topic_and_more'),
        ('posts', '0008_alter_post_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.header'),
        ),
        migrations.RunPython(sync_post_header),
        migrations.RemoveField(
            model_name='post',
            name='header',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='header_fk',
            new_name='header',
        ),
    ]
