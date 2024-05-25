# BalduApp/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('', ''), ('M', 'Чоловічий'), ('F', 'Жіночий')))
    interests = models.TextField(blank=True)
    marital_status = models.CharField(max_length=50, choices=(('', ''), ('S', 'Самотній/Самотня'), ('M', 'Одружений/Заміжня'), ('D', 'Розлучений/Розлучена'), ('W', 'Вдівець/Вдова')), blank=True)
    orientation = models.CharField(max_length=50, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Додано related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Додано related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )