from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Форма для реєстрації користувача, яка є підкласом UserCreationForm
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    email = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput())
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



# Форма для авторизації користувача (вхід)
class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']