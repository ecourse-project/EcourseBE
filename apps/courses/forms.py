from django import forms
from apps.courses.models import Course, Lesson


class CourseForm(forms.ModelForm):
    lessons_removed = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "price",
            "lessons",
            "lessons_removed",
            "thumbnail",
            "is_selling",
            "course_of_class",
        )

    def clean(self):
        cleaned_data = super().clean()
        lesson_removed_ids = set(cleaned_data.get("lessons_removed"))

        if lesson_removed_ids:
            lesson_ids = set([str(lesson.pk) for lesson in cleaned_data.get("lessons")])
            if lesson_ids.intersection(lesson_removed_ids):
                raise forms.ValidationError("Cannot remove lesson that belong to 'Chosen lessons'")

        Lesson.objects.filter(pk__in=list(lesson_removed_ids)).update(removed=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["lessons_removed"].choices = [
            (str(lesson.pk), lesson.__str__()) for lesson in Lesson.objects.filter(removed=False).order_by("name")
        ]
