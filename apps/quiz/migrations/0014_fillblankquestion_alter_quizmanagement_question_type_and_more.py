# Generated by Django 4.0.5 on 2023-09-28 09:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_useranswer_match_alter_useranswer_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='FillBlankQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('hidden_words', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Fill blank - Questions',
            },
        ),
        migrations.AlterField(
            model_name='quizmanagement',
            name='question_type',
            field=models.CharField(blank=True, choices=[('CHOICES', 'CHOICES'), ('MATCH', 'MATCH'), ('FILL', 'FILL')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='quizmanagement',
            name='fill_blank_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.fillblankquestion'),
        ),
    ]
