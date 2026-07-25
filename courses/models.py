from django.db import models
from django.utils.text import slugify
from core.choices import EducationLevel

class CourseLevel(models.TextChoices):

    DIPLOMA = "DIPLOMA", "Diploma"

    BACHELOR = "BACHELOR", "Bachelor"

    MASTER = "MASTER", "Master"

    PHD = "PHD", "PhD"

class EntryRequirement(models.TextChoices):

    SEE = "SEE", "SEE"

    PLUS_TWO = "PLUS_TWO", "+2"

    DIPLOMA = "DIPLOMA", "Diploma"

    BACHELOR = "BACHELOR", "Bachelor"

class Course(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    short_name = models.CharField(
        max_length=20,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField()

    duration_years = models.PositiveSmallIntegerField()

    level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
    )

    entry_requirement = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_name