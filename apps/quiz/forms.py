from django import forms

from apps.core.utils import remove_punctuation
from apps.quiz.models import FillBlankQuestion
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
            "content",
            "display_content",
            "hidden_words",
            "hidden",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            list_words = [w.get("word") for w in self.instance.hidden_words] if self.instance.hidden_words else []
            self.fields["hidden"].choices = [(i, remove_punctuation(word)) for i, word in enumerate(list_words, start=1)]
            self.initial["hidden"] = (
                [w.get("id") for w in self.instance.hidden_words if w.get("hidden")]
                if self.instance.hidden_words
                else []
            )

            self.fields["display_content"].initial = get_final_content(self.instance.hidden_words, res_default=self.instance.content)
