from django import forms
from .models import User


class UserModelForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput
    )
    phone = forms.CharField(
        label='Phone number',
        widget=forms.TextInput(attrs={'placeholder': '(optional)'}),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'password',
            'confirm_password'
        ]

        labels = {
            'email': 'E-mail',
        }

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError("Passwords must match")

            return cleaned_data

# class UserLoginForm(forms.Form):
#     username = forms.CharField(
#         label='Username',
#     )
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput,
#     )
#
# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(
#         label='Username',
#     )
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput,
#     )
