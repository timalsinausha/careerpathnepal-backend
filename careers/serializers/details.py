from rest_framework import serializers
from careers.serializers.summary import CareerCourseSerializer,CollegeSummarySerializer
from careers.models import Career
from colleges.models import College

class CareerDetailSerializer(serializers.ModelSerializer):

    recommended_courses = CareerCourseSerializer(
        source="career_courses",
        many=True,
        read_only=True,
    )

    top_colleges = serializers.SerializerMethodField()

    class Meta:

        model = Career

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "job_demand",
            "future_scope",
            "skills_required",
            "work_environment",
            "minimum_education_level",
            "recommended_courses",
            "top_colleges",
        )


    def get_top_colleges(self, obj):

        colleges = College.objects.filter(
            college_courses__course__career_courses__career=obj,
            college_courses__is_available=True,
        ).distinct()

        return CollegeSummarySerializer(
            colleges,
            many=True,
        ).data
