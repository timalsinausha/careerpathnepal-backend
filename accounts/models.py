"""
Responsible for:
Database structure
Relationships
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager
from django.conf import settings
from django.utils import timezone


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
    


class PasswordResetOTP(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_otps",
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(
        default=False
    )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} - {self.otp}"