"""
Responsible for:
Database structure
Relationships
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None

    ROLE_CHOICES = [
        ("student", "Student"),
        ("college", "College"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)

    contact_number = models.CharField(max_length=15)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "contact_number",
    ]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"