# Typing Imports
from typing import Dict

# Rest Framework Imports
from rest_framework import serializers
from rest_framework.request import Request

# SimpleJWT Imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Account Service Imports
from account_service.models import AccountUser

# Third Party Imports
from rest_api_payload import success_response


class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountUser
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def validate(self, attrs):
        
        # Get email and username from attrs
        email = attrs.get("email")
        username = attrs.get("username")
        
        """Check if user with email exists"""
        if AccountUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email exits already. Please try again!")
        
        """Checks if user with username exists"""
        if AccountUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username exits already. Please try again!")
        
        return super().validate(attrs)
    
    
class UserLoginObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        """The default result (access/refresh tokens)"""
        data = super(UserLoginObtainPairSerializer, self).validate(attrs)

        """Custom data you want to include"""
        data.update({"username": self.user.username})
        data.update({"email": self.user.email})
        data.update({"id": self.user.id})

        """Return custom data in the response"""
        payload = success_response(
            status="success", message="Login successful", data=data
        )
        return payload
    

class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        
        # Get email from attrs
        email = attrs.get("email")
        
        """Check if email does not exists"""
        if not AccountUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exits!")
        
        return super().validate(attrs)
    
    
class UserResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "New Password"},
    )
    repeat_new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Repeat New Password"},
    )
    

class UserChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Current Password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "New Password"},
    )
    repeat_new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Repeat New Password"},
    )