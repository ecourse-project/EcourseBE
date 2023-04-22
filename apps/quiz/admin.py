from django.contrib import admin

from apps.quiz.models import Quiz, Answer, AnswerChoices


@admin.register(AnswerChoices)
class AnswerChoicesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'choice',
    )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_filter = ("course",)
    search_fields = (
        "question",
        "course__name",
    )
    list_display = (
        'custom_question',
        'course',
    )

    def custom_question(self, obj):
        return " ".join(obj.question.split(" ")[:4]) + "..."


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = (
        "user__email",
    )
    list_display = (
        'user',
        'quiz',
        'choice',
    )




