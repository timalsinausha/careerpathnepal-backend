from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Course
from .serializer import CourseDetailSerializer, CourseListSerializer


class CourseDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, slug):

        try:
            course = Course.objects.get(
                slug=slug,
                is_active=True,
            )

        except Course.DoesNotExist:

            return Response(
                {
                    "message": "Course not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CourseDetailSerializer(course)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
class CourseListAPIView(APIView):

    def get(self, request):
        courses = Course.objects.all()

        serializer = CourseListSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)