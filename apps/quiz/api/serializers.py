from rest_framework import serializers

from apps.quiz.models import Quiz, AnswerChoices


class QuizSerializer(serializers.ModelSerializer):
    # correct_answer = serializers.CharField(required=False, source="correct_answer.choice")

    class Meta:
        model = Quiz
        fields = (
            "id",
            "course",
            "question_number",
            "question",
            "A",
            "B",
            "C",
            "D",
        )

