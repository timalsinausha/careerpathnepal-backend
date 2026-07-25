from rest_framework import serializers

from locations.models import Province, District


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = [
            "id",
            "name",
        ]


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = [
            "id",
            "name",
        ]