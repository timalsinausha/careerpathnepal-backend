"""
Responsible for:
Receiving requests
Calling the serializer
Returning responses
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .serializers import ChangePasswordSerializer
from .serializers import UserProfileUpdateSerializer
from student_profile.models import StudentProfile
from student_profile.serializers import CombinedProfileSerializer


class RegisterAPIView(APIView):

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user= serializer.save()

            StudentProfile.objects.create(user=user)

            return Response(
                {
                    "message": "User registered successfully.",
                    "role":"student"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            #user = serializer.validated_data["user"]

            #refresh = RefreshToken.for_user(user)

            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class UserProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data ={
            "user":request.user,
            "student_profile": request.user.student_profile,
        }

        serializer = CombinedProfileSerializer(data)

       # serializer = UserProfileSerializer(request.user)
   
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    


class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            request.user.set_password(
                serializer.validated_data["new_password"]
            )

            request.user.save()

            return Response(
                {
                    "message": "Password changed successfully."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    


class UserProfileUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        serializer = UserProfileUpdateSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

           
            serializer.save()

            return Response(
                {
                    "message": "Profile updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )