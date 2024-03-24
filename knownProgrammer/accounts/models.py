from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_dev = models.BooleanField(default=False) #true / false



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name","is_dev"]

    objects = CustomUserManager()

    def __str__(self):
        return f"User profile of {self.email}"





class ProgramerProfile(models.Model):
    EXP = {
        ("JUNIOR","JUNIOR"),
        ("MIDDLE","MIDDLE"),
        ("SENIOR","SENIOR"),
    }

    CODE = (
        ("javascript","javascript"),
        ("python","python"),
        ("java","java"),
        ("c","c"),
        ("c+","c+"),



    )

    FRAMEWORKS = (
        ("Django","Django"),
        ("Celery","Celery"),
        ("Flask","Flask"),

    )

    user_id = models.ForeignKey("CustomUser",on_delete=models.CASCADE)
    rating = models.IntegerField(default=None)
    description = models.TextField(max_length=5000)
    experience = models.CharField(max_length=100,choices=EXP)
    portfolio = models.URLField(max_length=1000)
    code_skils = MultiSelectField(choices=CODE,max_length=500)
    frameworks = MultiSelectField(choices=FRAMEWORKS,max_length=500)

    def __str__(self):
        return f"{self.user_id}"