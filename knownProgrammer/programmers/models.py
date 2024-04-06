from django.conf import settings

from django.db import models
from multiselectfield import MultiSelectField


class ProgrammerProfile(models.Model):
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
        ("RUST", "RUST"),
        ("Kotlin", "Kotlin"),
        ("HTML", "HTML"),
        ("CSS", "CSS"),
        ("TypeScript", "TypeScript"),
        ("Scala", "Scala"),
        ("SWIFT", "SWIFT"),

    )

    TECH_STACK = (
        ("Django", "Django"),
        ("Celery", "Celery"),
        ("Flask", "Flask"),
        ("FastAPI", "FastAPI"),
        ("Databases", "Databases"),
        ("Docker", "Docker"),
        ("Git | GitHub", "Git | GitHub"),
        ("Node.js", "Node.js"),
        ("React", "React"),
        ("Symphony", "Symphony"),
        ("Ruby on Rails", "Ruby on Rails"),
    )

    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='programmer_profile')
    wage = models.PositiveIntegerField()
    description = models.TextField(max_length=5000)
    experience = models.CharField(max_length=100, choices=EXP)
    portfolio = models.URLField(max_length=1000)
    programming_languages = MultiSelectField(choices=CODE, max_length=500)
    tech_stack = MultiSelectField(choices=TECH_STACK, max_length=500)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Programmer profile of {self.user_id.email} ({self.user_id.first_name} {self.user_id.last_name})"

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            total_ratings = sum(r.rating for r in ratings)
            avg = total_ratings / len(ratings)
            return avg.__round__(2)
        else:
            return 0

    def ratings_count(self):
        return self.ratings.count()

    def is_rated(self, user):
        return self.ratings.filter(user=user).exists()


class Rating(models.Model):
    programmer = models.ForeignKey(ProgrammerProfile, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ratings_given', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Rating for {self.programmer.user_id.email} by {self.user_id.email}"
