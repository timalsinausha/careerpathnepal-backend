from django.db import models
from django.utils.text import slugify

from core.choices import OwnershipType
from locations.models import Province,District


class College(models.Model):

    university = models.ForeignKey(
        "universities.University",
        on_delete=models.CASCADE,
        related_name="colleges",
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    short_name = models.CharField(
        max_length=50,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="colleges",
        null=True,
        blank=True
    )

    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name="colleges",
        null=True,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    logo = models.ImageField(
        upload_to="colleges/",
        null=True,
        blank=True,
    )



    established_year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    ownership = models.CharField(
        max_length=20,
        choices=OwnershipType.choices,
        default=OwnershipType.PRIVATE,
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
    


class CollegeCourse(models.Model):

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="college_courses",
    )

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="college_courses",
    )

    is_available = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "college",
                    "course",
                ],
                name="unique_college_course",
            ),
        ]

    def __str__(self):

        return (
            f"{self.college.name} → "
            f"{self.course.short_name}"
        )