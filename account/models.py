from django.db import models
from core.models import Base
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(Base, AbstractUser):
    name = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    phone_number = models.IntegerField(max_length=50)
    birthday = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    national_code = models.IntegerField()
    image = models.ImageField(upload_to='covers/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Address(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
    city = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
