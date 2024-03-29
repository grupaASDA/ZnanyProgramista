from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_dev = models.BooleanField(default=False) #true / false

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_dev"]

    objects = CustomUserManager()

    def __str__(self):
        return f"User profile of {self.email}"


class ProgramerProfile(models.Model):
    EXP = {
        ("Junior", "Junior"),
        ("Mid", "Mid"),
        ("Senior", "Senior"),
    }

    CODE = (
        ("JavaScript", "JavaScript"),
        ("Python", "Python"),
        ("Java", "Java"),
        ("C", "C"),
        ("C++", "C++"),
        ("C#", "C#"),
        ("R", "R"),
        ("PHP", "PHP"),
        ("SQL", "SQL"),
    )

    TECH_STACK = (
        ("Django", "Django"),
        ("Celery", "Celery"),
        ("Flask", "Flask"),
        ("FastAPI", "FastAPI"),
        ("Databases", "Databases"),
        ("Docker", "Docker"),
        ("Git | GitHub", "Git | GitHub"),
    )

    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='programmer_profile')
    wage_min = models.PositiveIntegerField()
    wage_max = models.PositiveIntegerField()
    rating = models.FloatField(default=0)
    description = models.TextField(max_length=5000)
    experience = models.CharField(max_length=100, choices=EXP)
    portfolio = models.URLField(max_length=1000)
    programming_languages = MultiSelectField(choices=CODE, max_length=500)
    tech_stack = MultiSelectField(choices=TECH_STACK, max_length=500)

    def __str__(self):
        return f"User profile of {self.user_id.email} ({self.user_id.first_name} {self.user_id.last_name})"
