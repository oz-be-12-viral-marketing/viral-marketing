from django.db import models

from apps.users.choices import ROLE


# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=25, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=20, choices=ROLE, default="USER")
    is_active = models.BooleanField(default=True)
