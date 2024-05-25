# BalduApp/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('', ''), ('M', 'Чоловічий'), ('F', 'Жіночий')))
    interests = models.TextField(blank=True)
    marital_status = models.CharField(max_length=50, choices=(('', ''), ('S', 'Самотній/Самотня'), ('M', 'Одружений/Заміжня'), ('D', 'Розлучений/Розлучена'), ('W', 'Вдівець/Вдова')), blank=True)
    orientation = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommended_to')
    created_at = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    disliked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disliked_by')