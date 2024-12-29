from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Reservation
from django.contrib.auth import authenticate


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

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

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['game', 'table', 'start_time', 'end_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
