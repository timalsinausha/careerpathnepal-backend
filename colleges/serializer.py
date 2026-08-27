from rest_framework import serializers

from courses.serializer import CollegeCourseSerializer
from .models import College



class CollegeDetailSerializer(serializers.ModelSerializer):

    university = serializers.CharField(
        source="university.name",
        read_only=True,
    )

    province = serializers.CharField(
        source="province.name",
        read_only=True,
    )

    district = serializers.CharField(
        source="district.name",
        read_only=True,
    )
    courses = CollegeCourseSerializer(
        source="college_courses",
        many=True,
        read_only=True,
    )

    class Meta:

        model = College

        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "university",
            "province",
            "district",
            "address",
            "description",
            "website",
            "email",
            "phone",
            "logo",
            "established_year",
            "ownership",
            "courses",
        )