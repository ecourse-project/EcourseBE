# Generated by Django 4.0.5 on 2022-09-18 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_rename_lesson_course_lessons_and_more'),
        ('carts', '0004_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='courses',
            field=models.ManyToManyField(blank=True, to='courses.course'),
        ),
    ]
