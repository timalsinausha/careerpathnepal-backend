from django.db import models
from django.utils.text import slugify
from assessment.models import AssessmentAttribute
from core.choices import EducationLevel
from courses.models import Course


class CareerCategory(models.TextChoices):

    TECHNOLOGY = "TECHNOLOGY", "Technology"

    ENGINEERING = "ENGINEERING", "Engineering"

    BUSINESS = "BUSINESS", "Business & Finance"

    HEALTHCARE = "HEALTHCARE", "Healthcare"

    EDUCATION = "EDUCATION", "Education"

    ARTS = "ARTS", "Arts & Design"

    LAW = "LAW", "Law"

    SOCIAL_SCIENCE = "SOCIAL_SCIENCE", "Social Science"

    SCIENCE = "SCIENCE", "Science"

    HOSPITALITY = "HOSPITALITY", "Hospitality & Tourism"

    AGRICULTURE = "AGRICULTURE", "Agriculture"

    OTHER = "OTHER", "Other"

class Career(models.Model):

    category = models.ForeignKey(
        "CareerCategory",
        on_delete=models.PROTECT,
        related_name="careers",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=150,
        unique=True,
    )
    career_category = models.CharField(
        max_length=30,
        choices=CareerCategory.choices,
    )
    slug = models.SlugField(
        max_length=170,
        unique=True,
        blank=True,
    )

    short_description = models.CharField(
        max_length=255,
    )

    description = models.TextField()
    job_demand = models.CharField(
     max_length=100,
     blank=True
    )

    skills_required = models.TextField(
     blank=True
    )

    work_environment = models.TextField(
     blank=True
    )

    future_scope = models.TextField(
        blank=True,
    )

    minimum_education_level = models.CharField(
     max_length=20,
     choices=EducationLevel.choices,
    )

    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    salary_currency = models.CharField(
        max_length=10,
        default="NPR",
    )

    salary_note = models.CharField(
     max_length=255,
     blank=True,
    )

    image = models.ImageField(
        upload_to="careers/",
        null=True,
        blank=True,
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
        return self.name
    

class CareerAttributeWeight(models.Model):

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name="attribute_weights",
    )

    attribute = models.ForeignKey(
        AssessmentAttribute,
        on_delete=models.CASCADE,
        related_name="career_weights",
    )

    weight = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "career",
                    "attribute",
                ],
                name="unique_career_attribute",
            ),
        ]

    def __str__(self):
        return (
            f"{self.career.name} - "
            f"{self.attribute.name} "
            f"({self.weight})"
        )
    
class CareerCourse(models.Model):

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name="career_courses",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="career_courses",
    )

    is_primary = models.BooleanField(
        default=False,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "career",
                    "course",
                ],
                name="unique_career_course",
            ),
        ]

    def __str__(self):
        return (
            f"{self.career.name} → "
            f"{self.course.short_name}"
        )
    
class CareerCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
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
        return self.name