from django.contrib.auth import login, password_validation
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import exceptions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from authuser.models import User
from typing import TypedDict


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["student_id", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str) -> str:
        if value is not None:
            password_validation.validate_password(value)
        return value

    def create(self, validated_data) -> User:
        user: User
        try:
            user = User.objects.create(
                student_id=validated_data["student_id"],
                email=validated_data["email"],
                name=validated_data["name"],
            )
        except IntegrityError:
            # By default this exception results in a response with the HTTP 400
            raise exceptions.ValidationError(
                "There is already an account with this student id or email address",
            )

        user.set_password(validated_data["password"])
        user.save()

        return user


class SignupView(APIView):
    """
    View to create a new user in the system.
    """

    def post(self, request):
        # used for validating and deserializing input, and for serializing output
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
