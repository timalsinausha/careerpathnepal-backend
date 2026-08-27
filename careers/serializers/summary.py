from rest_framework import serializers
from careers.models import Career
from courses.models import Course
from colleges.models import College
from careers.models import CareerCourse


class CareerSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Career
        fields = (
            "id",
            "name",
            "slug",
        )


class CourseSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "short_name",
        )


class CollegeSummarySerializer(serializers.ModelSerializer):
    province = serializers.CharField(source="province.name")
    district = serializers.CharField(source="district.name")

    class Meta:
        model = College
        fields = (
            "id",
            "name",
            "province",
            "district",
            "address",
        )



class CareerCourseSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        source="course.id",
        read_only=True,
    )

    name = serializers.CharField(
        source="course.name",
        read_only=True,
    )

    short_name = serializers.CharField(
        source="course.short_name",
        read_only=True,
    )

    slug = serializers.CharField(
        source="course.slug",
        read_only=True,
    )

    class Meta:

        model = CareerCourse

        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "is_primary",
        )