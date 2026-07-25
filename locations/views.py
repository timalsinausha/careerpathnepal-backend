from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from locations.models import Province, District
from locations.serializers import (
    ProvinceSerializer,
    DistrictSerializer,
)


class ProvinceListAPIView(APIView):

    def get(self, request):

        provinces = Province.objects.all()

        serializer = ProvinceSerializer(
            provinces,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    


class DistrictListAPIView(APIView):

    def get(self, request):

        province_id = request.query_params.get("province")

        if not province_id:
            return Response(
                {
                    "message": "Province ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        districts = District.objects.filter(
            province_id=province_id
        )

        serializer = DistrictSerializer(
            districts,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )