import os

import dotenv
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

dotenv.load_dotenv()
DEFAULT_AVATAR = os.getenv("DEFAULT_AVATAR")


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=11, unique=True, null=True)
    is_dev = models.BooleanField(default=False)
    avatar = models.CharField(max_length=1000, default=DEFAULT_AVATAR)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_dev"]

    objects = CustomUserManager()

    def __str__(self):
        return f"User profile of {self.email}"
