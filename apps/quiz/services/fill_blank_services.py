from string import punctuation

from apps.quiz.enums import ADMIN_DISPLAY_SUBSTRING

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


def get_final_content(hidden_words, substring=ADMIN_DISPLAY_SUBSTRING, res_default=""):
    if hidden_words:
        return " ".join(
            [
                w.get("word") if not w.get("hidden")else replace_word(w.get("word"), substring)
                for w in hidden_words
            ]
        )
    return res_default


def get_list_hidden(hidden_words):
    if not hidden_words:
        return []
    return [obj for obj in hidden_words if obj["hidden"]]


def check_correct(original, word):
    if (
            isinstance(original, str)
            and isinstance(word, str)
            and remove_punctuation(original).strip().lower() == remove_punctuation(word).strip().lower()
    ):
        return True
    return False
