from django import forms

from apps.courses.models import Course, Lesson
from apps.courses.services.admin import AdminCoursePermissons


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
        lesson_remove_ids = cleaned_data.get("lessons_remove")

        if lesson_remove_ids:
            for lesson in Lesson.objects.filter(pk__in=lesson_remove_ids):
                if lesson.courses.all().first():
                    raise forms.ValidationError(
                        "Cannot remove lesson that belong to 'Chosen lessons' of Course or Class"
                    )

        Lesson.objects.filter(pk__in=list(lesson_remove_ids)).update(removed=True)
