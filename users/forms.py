from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(forms.Form):
    phone = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Номер телефона", 'class': 'form-control', 'type': 'phone'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Пароль", 'class': 'form-control', 'type': 'password'}))


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Номер телефона", 'class': 'form-control', 'type': 'phone'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Имя", 'class': 'form-control', 'type': 'first_name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Фамилия", 'class': 'form-control', 'type': 'last_name'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Пароль", 'class': 'form-control', 'type': 'password1'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Пароль", 'class': 'form-control', 'type': 'password2'}))

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    phone = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Номер телефона", 'class': 'form-control', 'type': 'phone'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Имя", 'class': 'form-control', 'type': 'first_name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Фамилия", 'class': 'form-control', 'type': 'last_name_edit'}))

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name')
