from rest_framework import serializers

from apps.upload.api.serializers import UploadImageSerializer
from apps.quiz.models import (
    ChoicesQuizChoiceName,
    ChoicesQuizAnswer,
    ChoicesQuizQuestion,
    MatchColumnContent,
    MatchColumnQuestion,
    QuizManagement,
    ChoicesQuizUserAnswer,
)
from apps.quiz.services.choices_question_services import choices_quiz_data_processing
from apps.quiz.services.match_column_services import match_column_quiz_data_processing
from apps.quiz.services.services import quiz_data_processing


class ChoicesQuizChoiceNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoicesQuizChoiceName
        fields = (
            "id",
            "name",
        )


class ChoicesQuizAnswerSerializer(serializers.ModelSerializer):
    answer_image = UploadImageSerializer()
    choice_name = ChoicesQuizChoiceNameSerializer()

    class Meta:
        model = ChoicesQuizAnswer
        fields = (
            "id",
            "answer_type",
            "answer_text",
            "answer_image",
            "choice_name",
        )


class ChoicesQuizQuestionSerializer(serializers.ModelSerializer):
    choices = ChoicesQuizAnswerSerializer(many=True)
    content_image = UploadImageSerializer()

    class Meta:
        model = ChoicesQuizQuestion
        fields = (
            "course",
            "content_text",
            "content_image",
            "content_type",
            "choices",
        )

    def to_representation(self, instance):
        representation = super(ChoicesQuizQuestionSerializer, self).to_representation(instance)
        return choices_quiz_data_processing(representation)


class MatchColumnContentSerializer(serializers.ModelSerializer):
    content_image = UploadImageSerializer()

    class Meta:
        model = MatchColumnContent
        fields = (
            "id",
            "content_type",
            "content_text",
            "content_image",
        )

    def to_representation(self, instance):
        representation = super(MatchColumnContentSerializer, self).to_representation(instance)
        return match_column_quiz_data_processing(representation)


class MatchColumnQuestionSerializer(serializers.ModelSerializer):
    first_column = MatchColumnContentSerializer(many=True)
    second_column = MatchColumnContentSerializer(many=True)

    class Meta:
        model = MatchColumnQuestion
        fields = (
            "content",
            "first_column",
            "second_column",
        )


class QuizManagementSerializer(serializers.ModelSerializer):
    choices_question = ChoicesQuizQuestionSerializer()
    match_question = MatchColumnQuestionSerializer()

    class Meta:
        model = QuizManagement
        fields = (
            "id",
            "order",
            "question_type",
            "choices_question",
            "match_question",
        )

    def to_representation(self, instance):
        representation = super(QuizManagementSerializer, self).to_representation(instance)
        return quiz_data_processing(representation)




# class QuizResultResponseSerializer(serializers.ModelSerializer):
#     correct_answer = serializers.CharField(required=False, source="correct_answer.choice")
#
#     class Meta:
#         model = Quiz
#         fields = (
#             "id",
#             "correct_answer",
#         )
#
