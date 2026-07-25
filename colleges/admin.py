from django.contrib import admin

from .models import (
    College,
    CollegeCourse,
)

class CollegeCourseInline(admin.TabularInline):
    model = CollegeCourse
    extra = 1


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "university",
        "website",
        "is_active",
    )

    list_filter = (
        "university",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )


@admin.register(CollegeCourse)
class CollegeCourseAdmin(admin.ModelAdmin):

    list_display = (
        "college",
        "course",
        "is_available",
    )

    list_filter = (
        "course",
        "college__university",
        "is_available",
    )

    search_fields = (
        "college__name",
        "course__name",
    )