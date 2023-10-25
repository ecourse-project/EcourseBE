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
            "topic",
            "description",
            "price",
            "lessons",
            "lessons_removed",
            "thumbnail",
            "is_selling",
            "course_of_class",
            "test",
        )

    def clean(self):
        cleaned_data = super().clean()
        lesson_removed_ids = cleaned_data.get("lessons_removed")

        if lesson_removed_ids:
            for lesson in Lesson.objects.filter(pk__in=lesson_removed_ids):
                if lesson.courses.all().first():
                    raise forms.ValidationError(
                        "Cannot remove lesson that belong to 'Chosen lessons' of Course or Class"
                    )

        Lesson.objects.filter(pk__in=list(lesson_removed_ids)).update(removed=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_lesson = [
            (str(lesson.pk), lesson.__str__()) for lesson in Lesson.objects.filter(removed=False).order_by("name")
        ]
        self.fields["lessons"].choices = available_lesson
        self.fields["lessons_removed"].choices = available_lesson
