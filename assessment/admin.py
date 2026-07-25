from django.contrib import admin

from .models import AssessmentAttribute
from .models import (
    AssessmentAttribute,
    AssessmentQuestion,
    AssessmentOption,
    OptionScore,
    AssessmentAttempt,
    StudentAnswer,
    StudentAttributeScore,
)




@admin.register(AssessmentAttribute)
class AssessmentAttributeAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "code",
        "category",
        "is_active",
        "created_at",
    ]

    list_filter = [
        "category",
        "is_active",
    ]

    search_fields = [
        "name",
        "code",
    ]

    ordering = [
        "category",
        "name",
    ]


@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):

    list_display = [
        "order",
        "question_text",
        "is_active",
        "created_at",
    ]

    list_filter = [
        "is_active",
    ]

    search_fields = [
        "question_text",
    ]

    ordering = [
        "order",
    ]


@admin.register(AssessmentOption)
class AssessmentOptionAdmin(admin.ModelAdmin):

    list_display = [
        "question",
        "option_code",
        "option_text",
        "order",
    ]

    list_filter = [
        "question",
    ]

    search_fields = [
        "option_text",
        "option_code",
    ]

    ordering = [
        "question",
        "order",
    ]


@admin.register(OptionScore)
class OptionScoreAdmin(admin.ModelAdmin):

    list_display = [
        "option",
        "attribute",
        "score",
    ]

    list_filter = [
        "attribute",
    ]

    search_fields = [
        "option__option_text",
        "attribute__name",
    ]

    ordering = [
        "option",
        "-score",
    ]


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):

    list_display = [
        "student",
        "started_at",
        "completed_at",
        "is_completed",
    ]

    list_filter = [
        "is_completed",
    ]

    search_fields = [
        "student__user__email",
    ]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = [
        "attempt",
        "question",
        "selected_option",
        "answered_at",
    ]

    list_filter = [
        "question",
    ]

    search_fields = [
        "attempt__student__user__email",
        "question__question_text",
    ]

@admin.register(StudentAttributeScore)
class StudentAttributeScoreAdmin(admin.ModelAdmin):

    list_display = [
        "attempt",
        "attribute",
        "score",
        "percentage",
    ]

    list_filter = [
        "attribute",
    ]

    search_fields = [
        "attempt__student__user__email",
        "attribute__name",
    ]

    ordering = [
        "-percentage",
    ]