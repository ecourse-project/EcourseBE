# from apps.quiz.api.serializers import QuizSerializer
# from apps.quiz.models import (
#     MatchColumnMatchAnswer,
#     QuestionManagement,
# )
# from apps.quiz.enums import QUESTION_TYPE_MATCH
# from apps.core.general.enums import QUIZ_EXTRA_FIELDS
#
#
# class CustomQuizDataServices:
#     def __init__(self, instance, many: bool = False):
#         self.instance = instance
#         self.many = many
#
#     def custom_data(self):
#         data = QuizSerializer(instance=self.instance, many=self.many).data
#         return data
#
#     def match_question_correct_answer(self, data):
#         data_clone = data.copy()
#         if not self.instance:
#             return data
#         if not self.many:
#             data_clone = [data_clone]
#
#         match_question_mngt_id = [
#             question["id"] for question in data_clone
#             if question["question_type"] == QUESTION_TYPE_MATCH
#         ]
#         match_question_mngt = QuestionManagement.objects.filter(pk__in=match_question_mngt_id)
#         correct_answer = MatchColumnMatchAnswer.objects.filter(
#             match_question__in=match_question_mngt.values_list("match_question_id", flat=True)
#         )
#         return data_clone
#
#     def add_match_question_correct_answer(self):
#         pass