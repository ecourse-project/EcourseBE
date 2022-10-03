from django.contrib import admin

from apps.quiz.models import Quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'custom_question',
        'course',
    )

    def custom_question(self, obj):
        return obj.question[:20]



