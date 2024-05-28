# BalduApp/tests.py

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baldu.settings')
django.setup()

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from BalduApp.models import Chat, Message, Recommendation, Dislike
from BalduApp.forms import SignupForm, LoginForm, MessageForm, NewChatForm

User = get_user_model()

# Для забезпечення високої якості та надійності системи, було застосовано кілька методів тестування:

# 1. Модульне тестування
# Опис: Модульне тестування фокусується на перевірці окремих компонентів або модулів системи.
# Приклади тестів:
# - Тестування моделей: перевірка коректності створення, збереження та видалення об'єктів моделей.
# - Тестування форм: перевірка валідації форм та обробки введених даних.

class UserModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

    def test_user_creation(self):
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertTrue(self.user1.check_password('password123'))

    def test_chat_creation(self):
        chat = Chat.objects.create()
        chat.participants.add(self.user1, self.user2)
        self.assertIn(self.user1, chat.participants.all())
        self.assertIn(self.user2, chat.participants.all())

    def test_message_creation(self):
        chat = Chat.objects.create()
        chat.participants.add(self.user1, self.user2)
        message = Message.objects.create(chat=chat, sender=self.user1, content="Hello")
        self.assertEqual(message.content, "Hello")
        self.assertEqual(message.chat, chat)
        self.assertEqual(message.sender, self.user1)

    def test_recommendation_creation(self):
        recommendation = Recommendation.objects.create(user=self.user1, recommended_user=self.user2)
        self.assertEqual(recommendation.user, self.user1)
        self.assertEqual(recommendation.recommended_user, self.user2)

    def test_dislike_creation(self):
        dislike = Dislike.objects.create(user=self.user1, disliked_user=self.user2)
        self.assertEqual(dislike.user, self.user1)
        self.assertEqual(dislike.disliked_user, self.user2)


class SignupFormTest(TestCase):

    def test_signup_form_valid(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'age': 25,
            'gender': 'M',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_age(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'age': 17,
            'gender': 'M',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)


class LoginFormTest(TestCase):

    def test_login_form_valid(self):
        form_data = {'username': 'user', 'password': 'password'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_fields(self):
        form_data = {'username': 'user'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class MessageFormTest(TestCase):

    def test_message_form_valid(self):
        form_data = {'content': 'Hello, World!'}
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

class NewChatFormTest(TestCase):

    def test_new_chat_form_valid(self):
        form_data = {'username': 'testuser'}
        form = NewChatForm(data=form_data)
        self.assertTrue(form.is_valid())

# 2. Інтеграційне тестування
# Опис: Інтеграційне тестування перевіряє взаємодію між різними компонентами системи.
# Приклади тестів:
# - Тестування подань (views): перевірка коректності обробки запитів та генерації відповідей.
# - Тестування шаблонів: перевірка коректності рендерингу HTML-шаблонів з переданими даними.

class ViewTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BalduApp/register.html')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BalduApp/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {'username': 'testuser1', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {'username': 'testuser1', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BalduApp/login.html')
        self.assertContains(response, "Неправильний логін або пароль")

    def test_logout_view(self):
        self.client.login(username='testuser1', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_profile_view_get(self):
        self.client.login(username='testuser1', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BalduApp/profile.html')

    def test_main_page_view_get(self):
        self.client.login(username='testuser1', password='password123')
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BalduApp/main_page.html')

    def test_chat_detail_view_get(self):
        chat = Chat.objects.create()
        chat.participants.add(self.user1, self.user2)
        self.client.login(username='testuser1', password='password123')
        response = self.client.get(reverse('chat_detail', args=[chat.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'BalduApp/chat_detail.html')

# 3. Системне тестування
# Опис: Системне тестування охоплює перевірку всієї системи в цілому, включаючи функціональні та нефункціональні вимоги.
# Приклади тестів:
# - Перевірка реєстрації та аутентифікації користувачів.
# - Перевірка функціональності пошуку та підбору пар.
# - Перевірка системи повідомлень та обміну інформацією.

class SystemTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

    def test_user_registration_and_authentication(self):
        # Реєстрація
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'age': 25,
            'gender': 'M',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration

        # Аутентифікація
        response = self.client.post(reverse('login'), {'username': 'newuser', 'password': 'complex_password_123'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
