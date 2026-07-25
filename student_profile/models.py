from django.conf import settings
from django.db import models

from locations.models import Province, District
from core.choices import EducationLevel

class BudgetRange(models.TextChoices):
    BELOW_2_LAKHS = "BELOW_2_LAKHS", "Below NPR 2 Lakhs"
    TWO_TO_FOUR = "TWO_TO_FOUR", "NPR 2–4 Lakhs"
    FOUR_TO_SIX = "FOUR_TO_SIX", "NPR 4–6 Lakhs"
    SIX_TO_EIGHT = "SIX_TO_EIGHT", "NPR 6–8 Lakhs"
    ABOVE_8 = "ABOVE_8", "Above NPR 8 Lakhs"


class StudentProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    highest_education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        blank=True,
    )

    highest_education_institution = models.CharField(
        max_length=255,
        blank=True,
    )

    academic_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profiles",
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profiles",
    )

    budget_range = models.CharField(
        max_length=30,
        choices=BudgetRange.choices,
        blank=True,
    )

    is_profile_completed = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    def update_profile_completion_status(self):

        self.is_profile_completed = all([
            self.highest_education_level,
            self.highest_education_institution,
            self.academic_score,
            self.province,
            self.district,
            self.budget_range,
        ])

        self.save(update_fields=["is_profile_completed"])

    def __str__(self):
        return self.user.email