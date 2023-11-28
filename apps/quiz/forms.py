from django import forms
from django.utils.html import format_html

from apps.core.utils import remove_punctuation
from apps.quiz.models import FillBlankQuestion, QuestionManagement
from apps.quiz.services.fill_blank_services import get_final_content


class FillBlankQuestionForm(forms.ModelForm):
    hidden = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    display_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 10, "cols": 92, "readonly": True})
    )

    class Meta:
        model = FillBlankQuestion
        fields = (
            "author",
            "content",
            "display_content",
            "hidden_words",
            "hidden",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            list_words = [w.get("word") for w in self.instance.hidden_words] if self.instance.hidden_words else []
            self.fields["hidden"].choices = [(i, remove_punctuation(word)) for i, word in enumerate(list_words, start=1) if remove_punctuation(word)]
            self.initial["hidden"] = (
                [w.get("id") for w in self.instance.hidden_words if w.get("hidden")]
                if self.instance.hidden_words
                else []
            )
            self.initial["display_content"] = get_final_content(
                self.instance.content,
                self.instance.hidden_words,
                res_default=self.instance.content
            )


# class QuizManagementForm(forms.ModelForm):
#     class Meta:
#         model = QuizManagement
#         fields = "__all__"
#
#     def clean(self):
#         cleaned_data = super().clean()
#         course = cleaned_data.get('course')
#         lesson = cleaned_data.get('lesson')
#
#         if course and lesson and lesson not in course.lessons.all():
#             raise forms.ValidationError("Lesson do not belong to the course.")
