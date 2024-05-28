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

    def test_multiple_messages(self):
        chat = Chat.objects.create()
        chat.participants.add(self.user1, self.user2)
        message1 = Message.objects.create(chat=chat, sender=self.user1, content="Hello")
        message2 = Message.objects.create(chat=chat, sender=self.user2, content="Hi there")
        self.assertEqual(chat.messages.count(), 2)
        self.assertIn(message1, chat.messages.all())
        self.assertIn(message2, chat.messages.all())


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

    def test_signup_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'age': 25,
            'gender': 'M',
            'password1': 'complex_password_123',
            'password2': 'different_password_123',
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_signup_form_missing_fields(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

class LoginFormTest(TestCase):

    def test_login_form_valid(self):
        form_data = {'username': 'user', 'password': 'password'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_fields(self):
        form_data = {'username': 'user'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

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

    def test_new_chat_form_invalid_username(self):
        form_data = {'username': ''}
        form = NewChatForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
