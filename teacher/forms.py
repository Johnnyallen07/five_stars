from django import forms

from teacher.models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'school', 'subjects', 'introduction']

    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects', '')
        print(subjects)
        # Ensure subjects is a comma-separated string
        if not subjects:
            raise forms.ValidationError("Subjects cannot be empty.")
        return subjects
