from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Course, CustomUser


class TeacherRegisterForm(UserCreationForm):
    invite_code = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'invite_code']

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        correct_code = '6666'

        if invite_code != correct_code:
            raise forms.ValidationError("The invite code is incorrect.")

        return invite_code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        return user


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2


class SubscriptionForm(forms.Form):
    subscriptions = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
