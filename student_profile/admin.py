from django.contrib import admin

from student_profile.models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "highest_education_level",
        "province",
        "district",
        "is_profile_completed",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    list_filter = (
        "highest_education_level",
        "province",
        "is_profile_completed",
    )

    ordering = (
        "-created_at",
    )