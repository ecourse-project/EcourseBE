from django import forms

from apps.courses.models import Course, Lesson


class CourseForm(forms.ModelForm):
    lessons_remove = forms.ModelMultipleChoiceField(
        required=False,
        queryset=None,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Course
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        lesson_remove = cleaned_data.get("lessons_remove")

        if lesson_remove:
            for lesson in lesson_remove:
                if lesson.courses.all().first():
                    raise forms.ValidationError(
                        "Cannot remove lesson that belong to 'Chosen lessons' of Course or Class"
                    )

        lesson_remove.update(removed=True)
