from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_STUDENT = "student"
    ROLE_JUDGE = "judge"
    ROLE_VOLUNTEER = "volunteer"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_STUDENT, "Student"),
        (ROLE_JUDGE, "Judge"),
        (ROLE_VOLUNTEER, "Volunteer"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    school = models.CharField(max_length=120, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"
