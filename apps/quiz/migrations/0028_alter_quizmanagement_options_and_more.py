# Generated by Django 4.0.5 on 2023-11-02 15:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0086_course_structure'),
        ('quiz', '0027_fillblankquestion_created_fillblankquestion_modified'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizmanagement',
            options={'ordering': ['order'], 'verbose_name': 'Quiz', 'verbose_name_plural': 'Management'},
        ),
        migrations.RemoveField(
            model_name='quizmanagement',
            name='course',
        ),
        migrations.RemoveField(
            model_name='quizmanagement',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='quizmanagement',
            name='name',
        ),
        migrations.AlterField(
            model_name='matchcolumnquestion',
            name='first_column',
            field=models.ManyToManyField(blank=True, related_name='questions_from_first_col', to='quiz.matchcolumncontent'),
        ),
        migrations.AlterField(
            model_name='matchcolumnquestion',
            name='second_column',
            field=models.ManyToManyField(blank=True, related_name='questions_from_second_col', to='quiz.matchcolumncontent'),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course')),
                ('quiz_mngt', models.ManyToManyField(blank=True, to='quiz.quizmanagement')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quiz',
                'ordering': ['course', 'name'],
            },
        ),
        migrations.AlterField(
            model_name='choicesquizuseranswer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.AlterField(
            model_name='fillblankuseranswer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.AlterField(
            model_name='matchcolumnuseranswer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
    ]
