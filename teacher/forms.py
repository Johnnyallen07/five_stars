from django import forms

from teacher.models import Teacher, TeacherSchedule

'''
TeacherForm contains User, Teacher, and TeacherDisplay instances for teacher register and teacher profile
'''


class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=75)
    image = forms.ImageField(required=False)
    competitions = forms.CharField(required=False)
    subjects = forms.CharField(required=False)
    brief_subjects = forms.CharField(max_length=75)
    brief_introduction = forms.CharField(max_length=75)

    class Meta:
        model = Teacher
        fields = ['username', 'image', 'brief_subjects', 'brief_introduction', 'first_name', 'last_name', 'school',
                  'subjects', 'competitions', 'introduction']

    def __init__(self, *args, **kwargs):
        teacher_display_instance = kwargs.pop('teacher_display_instance', None)
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if teacher_display_instance:
            self.fields['brief_subjects'].initial = teacher_display_instance.brief_subjects
            self.fields['brief_introduction'].initial = teacher_display_instance.brief_introduction

        if user_instance:
            self.fields['username'].initial = user_instance.username

    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects', '')
        # Ensure subjects is a comma-separated string
        if not subjects:
            raise forms.ValidationError("Subjects cannot be empty.")
        return subjects

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['username'] = self.data.get('username')
        return cleaned_data


class TeacherScheduleForm(forms.ModelForm):
    class Meta:
        model = TeacherSchedule
        fields = ['available_slots']
        widgets = {
            'available_slots': forms.HiddenInput()  # Slots will be set via JavaScript and hidden in the form
        }
