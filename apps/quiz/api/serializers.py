from rest_framework import serializers

from apps.upload.api.serializers import UploadImageSerializer
from apps.quiz.models import (
    Quiz,
    ChoiceName,
    ChoicesAnswer,
    ChoicesQuestion,
    MatchColumnContent,
    MatchColumnQuestion,
    FillBlankQuestion,
    QuestionManagement,
)
from apps.quiz.services.choices_question_services import choices_question_data_processing
from apps.quiz.services.match_column_services import match_column_question_data_processing
from apps.quiz.services.fill_blank_services import get_final_content
from apps.quiz.services.services import question_data_processing
from apps.quiz.enums import RESPONSE_SUBSTRING


class ChoiceNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceName
        fields = (
            "id",
            "name",
        )


class ChoicesAnswerSerializer(serializers.ModelSerializer):
    answer_image = UploadImageSerializer()
    choice_name = ChoiceNameSerializer()

    class Meta:
        model = ChoicesAnswer
        fields = (
            "id",
            "answer_type",
            "answer_text",
            "answer_image",
            "choice_name",
        )


class ChoicesQuestionSerializer(serializers.ModelSerializer):
    choices = ChoicesAnswerSerializer(many=True)
    content_image = UploadImageSerializer()

    class Meta:
        model = ChoicesQuestion
        fields = (
            "content_text",
            "content_image",
            "content_type",
            "choices",
        )

    def to_representation(self, instance):
        representation = super(ChoicesQuestionSerializer, self).to_representation(instance)
        return choices_question_data_processing(representation)


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
        return match_column_question_data_processing(representation)


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


class FillBlankQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillBlankQuestion
        fields = (
            "content",
            "hidden_words",
        )

    def to_representation(self, instance):
        representation = super(FillBlankQuestionSerializer, self).to_representation(instance)
        representation["content"] = get_final_content(instance.hidden_words, RESPONSE_SUBSTRING)
        return question_data_processing(representation)


class QuestionManagementSerializer(serializers.ModelSerializer):
    choices_question = ChoicesQuestionSerializer()
    match_question = MatchColumnQuestionSerializer()
    fill_blank_question = FillBlankQuestionSerializer()

    class Meta:
        model = QuestionManagement
        fields = (
            "id",
            "order",
            "time_limit",
            "question_type",
            "choices_question",
            "match_question",
            "fill_blank_question",
        )

    def to_representation(self, instance):
        representation = super(QuestionManagementSerializer, self).to_representation(instance)
        return question_data_processing(representation)


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionManagementSerializer(source="question_mngt", many=True)

    class Meta:
        model = Quiz
        fields = (
            "id",
            "name",
            "questions",
        )