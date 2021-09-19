from django.contrib.auth import authenticate
from django.db import models
from django.db.models import fields
from rest_framework import serializers, exceptions
from django.contrib.auth import password_validation

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializing user data"""

    class Meta:
        model = User
        exclude = (
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "last_login",
        )


class SignupSerializer(serializers.ModelSerializer):
    """Signup information serializer"""

    password1 = serializers.CharField(
        max_length=128, min_length=8, required=True, write_only=True
    )

    password2 = serializers.CharField(
        max_length=128, min_length=8, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password1",
            "password2",
        ]

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def save(self, request):
        try:
            user = User(
                email=self.validated_data["email"],
                username=self.validated_data["email"],
            )
        except Exception as e:
            raise serializers.ValidationError({"error": e.args})

        password1 = self.validated_data["password1"]
        password2 = self.validated_data["password2"]

        try:
            self.validate_password(password1)
        except Exception as e:
            raise serializers.ValidationError({"password": e.args})

        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        user.set_password(password1)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializing the login information"""

    email = serializers.EmailField(min_length=3, max_length=256)
    password = serializers.CharField(write_only=True, min_length=8, max_length=256)

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is not active"
                    raise exceptions.ValidationError(msg)

            else:
                msg = "Wrong credentials"
                raise exceptions.AuthenticationFailed(msg)
        else:
            msg = "Username and Password must be entered"
            raise exceptions.ValidationError(msg)

        return data
