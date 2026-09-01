"""
Responsible for:
Receiving requests
Calling the serializer
Returning responses
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, ResetPasswordSerializer, VerifyOTPSerializer
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer
from .serializers import UserProfileUpdateSerializer
from student_profile.models import StudentProfile
from student_profile.serializers import CombinedProfileSerializer
from .models import PasswordResetOTP
from .serializers import ForgotPasswordSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
import random




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
    



User = get_user_model()


class ForgotPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]

        user = User.objects.get(
            email=email
        )

        # Generate 6 digit OTP
        otp = str(
            random.randint(100000, 999999)
        )

        # Expire after 5 minutes
        expires_at = (
            timezone.now()
            + timedelta(minutes=5)
        )

        # Remove old OTPs
        PasswordResetOTP.objects.filter(
            user=user,
            is_verified=False,
        ).delete()

        # Create new OTP
        PasswordResetOTP.objects.create(
            user=user,
            otp=otp,
            expires_at=expires_at,
        )

        # Send email
        send_mail(
            subject="CareerNepal Password Reset OTP",
            message=(
                f"Your CareerNepal password reset OTP is: {otp}\n\n"
                "This OTP is valid for 5 minutes.\n\n"
                "If you did not request a password reset, "
                "please ignore this email."
            ),
            from_email=None,
            recipient_list=[email],
        )

        return Response(
            {
                "message": "OTP sent successfully."
            },
            status=status.HTTP_200_OK,
        )
    


class VerifyOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_record = serializer.validated_data[
            "otp_record"
        ]

        # Mark OTP as verified
        otp_record.is_verified = True
        otp_record.save(
            update_fields=["is_verified"]
        )

        return Response(
            {
                "message": "OTP verified successfully."
            },
            status=status.HTTP_200_OK,
        )
    

class ResetPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        otp_record = serializer.validated_data["otp_record"]

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        # Prevent OTP from being reused
        otp_record.delete()

        return Response(
            {
                "message":
                "Password reset successfully."
            },
            status=status.HTTP_200_OK,
        )