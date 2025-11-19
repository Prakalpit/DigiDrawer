from django import forms
from django.contrib.auth.forms import AuthenticationForm


class DigiDrawerLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-400",
            "placeholder": "Username",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-400",
            "placeholder": "Password",
        })
    )
