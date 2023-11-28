from uuid import uuid4
from typing import List
from string import punctuation

from django.db.models import Q

from apps.quiz.enums import ADMIN_DISPLAY_SUBSTRING, QUESTION_TYPE_FILL
from apps.quiz.models import (
    Quiz,
    QuestionManagement,
    FillBlankUserAnswer,
    FillBlankQuestion,
)
from apps.core.utils import remove_punctuation


def split_content(content: str):
    if not content:
        return content

    list_words = content.split()
    return [{"id": i, "word": w, "hidden": False} for i, w in enumerate(list_words, start=1)]


# Replace by substring: "!word)" =>  "!...)"
def replace_word(word, substring):
    first = last = ""
    if not word:
        return ""

    if word[0] in punctuation and word[-1] not in punctuation:
        first = word[0]
    elif word[0] not in punctuation and word[-1] in punctuation:
        last = word[-1]
    elif word[0] in punctuation and word[-1] in punctuation:
        first = word[0]
        last = word[-1]
    return f"{first}{substring}{last}"


def get_final_content(original_content, hidden_words, substring=ADMIN_DISPLAY_SUBSTRING, res_default=""):
    res = []
    content_split = original_content.split()
    for item in zip(content_split, hidden_words):
        original = item[0]
        hidden = item[1]
        if item[1].get("hidden"):
            original = original.replace(hidden.get("word"), substring)
        res.append(original)

    return " ".join(res)


    # if hidden_words:
    #     return " ".join(
    #         [
    #             w.get("word") if not w.get("hidden") else substring  # replace_word(w.get("word"), substring)
    #             for w in hidden_words
    #         ]
    #     )
    # return res_default


def get_list_hidden(hidden_words):
    if not hidden_words:
        return []
    return [obj for obj in hidden_words if obj["hidden"]]


def check_correct(original, word):
    if (
            isinstance(original, str)
            and isinstance(word, str)
            # and original.lower().strip() == word.lower().strip()
            and remove_punctuation(original).strip().lower() == remove_punctuation(word).strip().lower()
    ):
        return True
    return False


def fill_question_processing(data: list, user):
    res = {}
    for question in data:
        pk = str(uuid4())
        instance = FillBlankQuestion(
            pk=pk,
            title=question.get("title"),
            content=question.get("content"),
            hidden_words=question.get("hidden_words"),
            author=user,
        )
        res[pk] = {
            "order": question.get("order", 1),
            "time_limit": question.get("time_limit", 10),
            "FillBlankQuestion": instance,
        }
    return res


def store_fill_question(data: list, user):
    res = fill_question_processing(data, user)
    list_question = []
    list_question_mngt = []
    for pk, info in res.items():
        list_question.append(info["FillBlankQuestion"])
        list_question_mngt.append(
            QuestionManagement(
                order=info["order"],
                question_type=QUESTION_TYPE_FILL,
                fill_blank_question=info["FillBlankQuestion"],
                time_limit=info["time_limit"],
            )
        )
    if list_question:
        FillBlankQuestion.objects.bulk_create(list_question)
    return list_question_mngt


def delete_fill_question(question_mngt: QuestionManagement):
    if question_mngt and question_mngt.fill_blank_question:
        question_mngt.fill_blank_question.delete()
        question_mngt.delete()


def user_correct_question_fill(quiz: Quiz, user, created) -> List:
    fill_question = quiz.question_mngt.filter(
        Q(
            question_type=QUESTION_TYPE_FILL,
            fill_blank_question__isnull=False,
        )
        & ~Q(
            Q(fill_blank_question__hidden_words=[])
            | Q(fill_blank_question__hidden_words__isnull=True)
        )
    )
    if not fill_question:
        return []

    user_fill_answers = FillBlankUserAnswer.objects.filter(
        Q(
            created=created,
            user=user,
            question__in=fill_question,
        )
    )
    user_fill_answers_dict = {str(answer.question_id): answer for answer in user_fill_answers}

    res = []
    for question_mngt in fill_question:
        question = question_mngt.fill_blank_question
        question_mngt_id = str(question_mngt.id)
        hidden_words = get_list_hidden(question.hidden_words)
        hidden_words_values = [w["word"] for w in hidden_words]
        info = {
                "question_id": question_mngt_id,
                "user_answer": [],
                "correct_answer": [remove_punctuation(w) for w in hidden_words_values],
                "correct": 0,
                "total": len(hidden_words),
        }

        answer = user_fill_answers_dict.get(question_mngt_id)
        if answer:
            correct = 0
            user_answer = answer.words or []
            user_answer_copy = user_answer.copy()
            for word in hidden_words_values:
                if not user_answer_copy:
                    break
                if check_correct(word, user_answer_copy[0]):
                    correct += 1
                user_answer_copy.pop(0)

            info["user_answer"] = user_answer
            info["correct"] = correct

        res.append(info)

    # for answer in user_fill_answers:
    #     question = answer.question.fill_blank_question
    #     correct = 0
    #     user_answer = answer.words or []
    #     user_answer_copy = user_answer.copy()
    #     hidden_words = get_list_hidden(question.hidden_words)
    #     hidden_words_values = [w["word"] for w in hidden_words]
    #     for word in hidden_words_values:
    #         if not user_answer_copy:
    #             break
    #         if check_correct(word, user_answer_copy[0]):
    #             correct += 1
    #         user_answer_copy.pop(0)
    #
    #     res.append(
    #         {
    #             "question_id": str(answer.question_id),
    #             "user_answer": user_answer,
    #             "correct_answer": [remove_punctuation(w) for w in hidden_words_values],
    #             "correct": correct,
    #             "total": len(hidden_words),
    #         }
    #     )

    return res
