from rest_framework import serializers

from careers.models import Career


class CareerRecommendationCareerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Career
        fields = (
            "id",
            "name",
            "slug",
        )


class RecommendedCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    short_name= serializers.CharField()
    is_primary = serializers.BooleanField()



class RecommendedCollegeSerializer(serializers.Serializer):

    id = serializers.IntegerField()

    name = serializers.CharField()

    province = serializers.CharField()

    district = serializers.CharField()

    address = serializers.CharField()


    
class RecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="career.id")
    career = CareerRecommendationCareerSerializer()
   # career = serializers.CharField(source="career.name")
    match_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    eligible = serializers.BooleanField()
    minimum_education_level = serializers.CharField()
    next_step = serializers.CharField()

    recommended_courses = RecommendedCourseSerializer(
        many=True,
    )

    top_colleges = RecommendedCollegeSerializer(
        many=True,
    )




