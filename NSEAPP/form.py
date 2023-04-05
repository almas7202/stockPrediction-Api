from django.contrib.auth.forms import *
from .models import *
from django import forms
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control required', 'placeholder': '*Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control required', 'placeholder': '*Enter Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
            'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': '*Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': '*Enter Firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': '*Enter Lastname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control required', 'placeholder': '*Enter E-Mail'}),
        }


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control required', 'placeholder': '*Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control required', 'placeholder': '*Enter Password'}))

