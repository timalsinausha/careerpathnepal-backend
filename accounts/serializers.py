"""
Responsible for:
Validating incoming data
Converting JSON ↔ Python objects
Checking business rules
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
#from django.contrib.auth import authenticate
from .models import PasswordResetOTP, User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "password",
            "confirm_password",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        """
        Validate data involving multiple fields.
        """

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        
        
        user= User(
            first_name=attrs.get("first_name"),
            last_name=attrs.get("last_name"),
            email=attrs.get("email"),
        )

        # Use Django's built-in password validators
        
        validate_password(attrs["password"], user=user)

        return attrs

    def create(self, validated_data):
        """
        Create a new user.
        """

        validated_data.pop("confirm_password")

        return User.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )
        
        if not user.check_password(password):
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        #attrs["user"] = user
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
            }
        }

        #return attrs
    

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "role"
        ]


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):

     user = self.context["request"].user

     if not user.check_password(attrs["current_password"]):
        raise serializers.ValidationError(
                {"current_password": "Current password is incorrect."}
            )

     validate_password(attrs["new_password"], user)

     return attrs
    


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "contact_number",
        ]


User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No account found with this email."
            )

        return value
    


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField(
        max_length=6,
        min_length=6,
    )

    def validate(self, attrs):

        email = attrs["email"]
        otp = attrs["otp"]

        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No account found with this email."}
            )

        try:
            otp_record = PasswordResetOTP.objects.filter(
                user=user,
                is_verified=False,
            ).latest("created_at")

        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError(
                {"otp": "No valid OTP found."}
            )

        # Check expiry
        if otp_record.is_expired():
            raise serializers.ValidationError(
                {"otp": "OTP has expired. Please request a new OTP."}
            )

        # Check OTP
        if otp_record.otp != otp:
            raise serializers.ValidationError(
                {"otp": "Invalid OTP."}
            )

        attrs["user"] = user
        attrs["otp_record"] = otp_record

        return attrs
    
class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    new_password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs["email"]
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]

        # Check passwords
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        # Find user
        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "email":
                    "No account found with this email."
                }
            )

        # Check OTP verification
        try:
            otp_record = PasswordResetOTP.objects.filter(
                user=user,
                is_verified=True,
            ).latest("created_at")

        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "otp":
                    "Please verify OTP before resetting password."
                }
            )

        # Validate new password
        validate_password(
            new_password,
            user
        )

        attrs["user"] = user
        attrs["otp_record"] = otp_record

        return attrs