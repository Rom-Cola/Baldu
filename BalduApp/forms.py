# BalduApp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Ім\'я'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Прізвище'
    )
    age = forms.IntegerField(
        required=True,
        min_value=18,
        error_messages={'min_value': 'Вік повинен бути не менше 18 років.'},
        label='Вік'
    )
    gender = forms.ChoiceField(
        choices=(('', ''), ('M', 'Чоловічий'), ('F', 'Жіночий')),
        required=True,
        label='Стать'
    )
    interests = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Інформація про себе'
    )
    marital_status = forms.ChoiceField(
        choices=(('', ''), ('S', 'Самотній/Самотня'), ('M', 'Одружений/Заміжня'), ('D', 'Розлучений/Розлучена'), ('W', 'Вдівець/Вдова')),
        required=False,
        label='Сімейний статус'
    )
    orientation = forms.CharField(
        required=False,
        label='Орієнтація'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'age', 'gender', 'interests', 'marital_status', 'orientation', 'password1', 'password2']
        labels = {
            'username': 'Логін',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля'
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('Вік повинен бути не менше 18 років.')
        return age


class LoginForm(forms.Form):
    username = forms.CharField(label='Логін')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class NewChatForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class LikeForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

class DislikeForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'gender', 'interests', 'marital_status', 'orientation']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('Вік повинен бути не менше 18 років.')
        return age