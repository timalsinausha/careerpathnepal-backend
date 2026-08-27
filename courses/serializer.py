from rest_framework import serializers

from colleges.models import CollegeCourse

from .models import Course

class CourseDetailSerializer(serializers.ModelSerializer):

    colleges = serializers.SerializerMethodField()

    class Meta:

        model = Course

        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "description",
            "duration_years",
            "level",
            "entry_requirement",
            "colleges",
        )

    def get_colleges(self, obj):

        college_courses = (
            obj.college_courses
            .filter(
                is_available=True,
                college__is_active=True,
            )
            .select_related(
                "college",
                "college__province",
                "college__district",
            )
        )

        return CourseCollegeSerializer(
            college_courses,
            many=True,
        ).data
    


class CourseCollegeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        source="college.id",
        read_only=True,
    )

    name = serializers.CharField(
        source="college.name",
        read_only=True,
    )

    short_name = serializers.CharField(
        source="college.short_name",
        read_only=True,
    )

    slug = serializers.CharField(
        source="college.slug",
        read_only=True,
    )

    province = serializers.CharField(
        source="college.province.name",
        read_only=True,
    )

    district = serializers.CharField(
        source="college.district.name",
        read_only=True,
    )

    address = serializers.CharField(
        source="college.address",
        read_only=True,
    )

    class Meta:

        model = CollegeCourse

        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "province",
            "district",
            "address",
        )

class CollegeCourseSerializer(serializers.ModelSerializer):

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
        model = CollegeCourse

        fields = (
            "id",
            "name",
            "short_name",
            "slug",
        )