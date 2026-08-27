from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import College
from .serializer import CollegeDetailSerializer


class CollegeDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, slug):

        try:

            college = College.objects.get(
                slug=slug,
                is_active=True,
            )

        except College.DoesNotExist:

            return Response(
                {
                    "message": "College not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CollegeDetailSerializer(
            college
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )