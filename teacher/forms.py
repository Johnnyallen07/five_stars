from django import forms

from teacher.models import Teacher, TeacherSchedule


class TeacherForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Teacher
        fields = ['image', 'first_name', 'last_name', 'school', 'subjects', 'introduction']

    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects', '')
        print(subjects)
        # Ensure subjects is a comma-separated string
        if not subjects:
            raise forms.ValidationError("Subjects cannot be empty.")
        return subjects


class TeacherScheduleForm(forms.ModelForm):
    class Meta:
        model = TeacherSchedule
        fields = ['slots']
        widgets = {
            'slots': forms.HiddenInput()  # Slots will be set via JavaScript and hidden in the form
        }
