from typing import Optional, Type
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import Token, RefreshToken
from django.conf import settings
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    token_class: Optional[Type[Token]] = RefreshToken

    default_error_message = {
        "no_active_account": "No active account found with the provided credentials"
    }

    class Meta:
        model = User
        fields = ["email", "password"]


    def default_user_authentication_rule(self, user):
        return user is not None and user.is_active


    @classmethod
    def get_tokens(cls, user):
        token = cls.token_class.for_user(user)
        return token


    def validate(self, attrs):
        data = super().validate(attrs)

        username = data.get("email", None)
        password = data.get("password", None)

        auth_kwargs = {
            "username": username,
            "password": password
        }

        self.user = authenticate(request=self.context['request'], **auth_kwargs)

        if not self.default_user_authentication_rule(self.user):
            raise serializers.ValidationError(self.default_error_message['no_active_account'], 'no_active_account')
        
        # Return a user object if user found
        refresh = self.get_tokens(self.user)

        data['message'] = 'Login successful'
        data['token'] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        # Remove password and email fields from validated data
        data.pop('password')
        data.pop('email')
        
        # Update last login
        if settings.SIMPLE_JWT['UPDATE_LAST_LOGIN']:
            self.user.last_login = timezone.now()
            self.user.save()
        
        user_dict = UserSerializer(self.user).to_representation(self.user)
        data['user'] = user_dict
        return data
    

class SignupSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation']

    def validate(self, attrs):
        data = super().validate(attrs)
        username = data.get('email')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password!= password_confirmation:
            raise serializers.ValidationError("Passwords do not match")
        return data
    

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        return user
    

