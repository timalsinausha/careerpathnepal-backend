from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "short_name",
        "name",
        "level",
        "entry_requirement",
        "duration_years",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    list_filter = (
        "level",
        "entry_requirement",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
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
                    "short_name",
                    "slug",
                    "description",
                ),
            },
        ),
        (
            "Course Details",
            {
                "fields": (
                    "level",
                    "entry_requirement",
                    "duration_years",
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