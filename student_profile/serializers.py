from rest_framework import serializers

from accounts.serializers import UserProfileSerializer
from locations.models import Province, District
from locations.serializers import ProvinceSerializer, DistrictSerializer
from student_profile.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Read Serializer (GET)
    Returns nested Province and District objects.
    """

    province = ProvinceSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "highest_education_level",
            "highest_education_institution",
            "academic_score",
            "province",
            "district",
            "budget_range",
            "is_profile_completed",
        ]


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Write Serializer (PATCH)
    Accepts Province and District IDs.
    """

    province = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all()
    )

    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all()
    )

    class Meta:
        model = StudentProfile

        fields = [
            "highest_education_level",
            "highest_education_institution",
            "academic_score",
            "province",
            "district",
            "budget_range",
        ]

    def validate(self, attrs):
        """
        Ensure the selected district belongs to the selected province.
        """

        province = attrs.get(
            "province",
            self.instance.province if self.instance else None
        )

        district = attrs.get(
            "district",
            self.instance.district if self.instance else None
        )

        if province and district:
            if district.province != province:
                raise serializers.ValidationError(
                    {
                        "district": "Selected district does not belong to the selected province."
                    }
                )

        return attrs


class CombinedProfileSerializer(serializers.Serializer):
    """
    Combines User and Student Profile.
    """

    user = UserProfileSerializer()

    student_profile = StudentProfileSerializer() 