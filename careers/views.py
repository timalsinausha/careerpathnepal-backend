from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from careers.models import Career
from careers.serializers.recommendation_serializers import RecommendationSerializer
from careers.serializers.details import CareerDetailSerializer
from careers.services.recommendation_service import (
    CareerRecommendationService,
)


class RecommendationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        service = CareerRecommendationService(request.user)

        recommendations = service.get_recommendations()

        serializer = RecommendationSerializer(
            recommendations[:10],
            many=True,
        )

        return Response(serializer.data)
    

class CareerDetailAPIView(RetrieveAPIView):

   # permission_classes = [IsAuthenticated]

    serializer_class = CareerDetailSerializer

    queryset = (
     Career.objects.filter(
        is_active=True,
     )
     .prefetch_related(
        "career_courses__course",
     )
    )

    lookup_field = "slug"