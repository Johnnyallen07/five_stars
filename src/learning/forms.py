from django import forms
from .models import MaterialPost
from five_stars.models import CustomUser


class SavePost(forms.ModelForm):
    class Meta:
        model = MaterialPost
        fields = ("course_title", "title", "description", "file_path")
