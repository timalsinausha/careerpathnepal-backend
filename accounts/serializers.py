"""
Responsible for:
Validating incoming data
Converting JSON ↔ Python objects
Checking business rules
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
#from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

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


    