from django import forms
from .models import User
from django.contrib.auth import authenticate


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        min_length=3,
        required=True
    )
    first_name = forms.CharField(
        required=True
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(optional)'}),
    )
    email = forms.EmailField(
        label='E-mail',
        required=True
    )
    phone = forms.CharField(
        label='Phone number',
        widget=forms.TextInput(attrs={'placeholder': '(optional)'}),
        required=False,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords must match")

        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=50
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise forms.ValidationError("Wrong username or password")
        return cleaned_data
