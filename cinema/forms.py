from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    identifier = forms.CharField(label='Имя пользователя или email')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput)