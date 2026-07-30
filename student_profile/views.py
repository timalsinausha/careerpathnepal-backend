from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from student_profile.serializers import (
    StudentProfileSerializer,
    StudentProfileUpdateSerializer,
)

class StudentProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile = request.user.student_profile

        serializer = StudentProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class StudentProfileUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def patch(self, request):
        profile = request.user.student_profile

        serializer = StudentProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            profile = serializer.save()

            return Response(
                {
                    "message": "Student profile updated successfully.",
                    "data": StudentProfileSerializer(profile).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )