from django import forms

from five_stars.models import CustomUser


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]
