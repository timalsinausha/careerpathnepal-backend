from django.contrib import admin

from locations.models import Province, District


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "id",
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "province",
        "created_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "province",
    )

    ordering = (
        "province",
        "name",
    )