from django.contrib import admin

from apps.quiz.models import Quiz, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'custom_question',
        'course',
    )

    def custom_question(self, obj):
        return obj.question[:20]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'choice',
    )




