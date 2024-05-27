# BalduApp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Логін'
    )
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
        widget=forms.Textarea(attrs={'maxlength': '200'}),
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
    username = forms.CharField(max_length=30, label='Username')

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'maxlength': '200',
            'placeholder': 'Введіть повідомлення: '
        }),
        required=False,
        label='Ваше повідомлення'
    )

    class Meta:
        model = Message
        fields = ['content']
        labels = {
            'content': 'Введіть повідомлення: '
        }

class LikeForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

class DislikeForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Логін'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'age', 'gender', 'interests', 'marital_status', 'orientation', 'profile_photo']
        labels = {
            'username': 'Логін',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'age': 'Вік',
            'gender': 'Гендер',
            'interests': 'Про себе',
            'marital_status': 'Сімейний статус',
            'orientation': 'Оріентація'
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('Вік повинен бути НЕ МЕНШЕ 18 років.')
        if age > 118:
            raise forms.ValidationError('Вік повинен бути НЕ БІЛЬШЕ 118 років.')
        return age
