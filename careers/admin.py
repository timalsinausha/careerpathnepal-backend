from django.contrib import admin
from .models import (
    Career,
    CareerAttributeWeight,
    CareerCourse,
    CareerCategory
)


class CareerAttributeWeightInline(admin.TabularInline):

    model = CareerAttributeWeight

    extra = 1


class CareerCourseInline(admin.TabularInline):

    model = CareerCourse

    extra = 1


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "minimum_education_level",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    list_filter = (
        "minimum_education_level",
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "image",  # Remove this line if your model doesn't have an image field.
                ),
            },
        ),
        (
            "Career Information",
            {
                "fields":(
                    "job_demand",
                    "future_scope",
                    "skills_required",
                    "work_environment",
                ),
            },
        ),
        (
            "Career Classification",
            {
                "fields":(
                    "category",
                ),
            },
        ),
        (
            "Education Requirement",
            {
                "fields": (
                    "minimum_education_level",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    inlines = [
        CareerAttributeWeightInline,
        CareerCourseInline,
    ]

@admin.register(CareerAttributeWeight)
class CareerAttributeWeightAdmin(admin.ModelAdmin):

    list_display = (
        "career",
        "attribute",
        "weight",
    )

    list_filter = (
        "career",
        "attribute__category",
    )

    search_fields = (
        "career__name",
        "attribute__name",
    )

@admin.register(CareerCourse)
class CareerCourseAdmin(admin.ModelAdmin):

    list_display = (
        "career",
        "course",
        "is_primary",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "career__name",
        "course__name",
    )

@admin.register(CareerCategory)
class CareerCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )