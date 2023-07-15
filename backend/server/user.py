from django.contrib.auth import login, password_validation
from django.shortcuts import render
from rest_framework import exceptions, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from authuser.models import User


class SignupSerializer(serializers.Serializer):
    name: serializers.Field = serializers.CharField(max_length=128)
    student_id: serializers.Field = serializers.CharField(max_length=9)
    email: serializers.Field = serializers.EmailField()
    password: serializers.Field = serializers.CharField(allow_null=True, required=True)

    def validate_password(self, value):
        if value is not None:
            password_validation.validate_password(value)
        return value

    def create(self, validated_data, **kwargs):
        user: User
        try:
            user = User.objects.create(
                student_id=validated_data["student_id"],
                email=validated_data["email"],
                name=validated_data["name"],
            )
        except IntegrityError:
            raise exceptions.ValidationError(
                "There is already an account with this student id or email address",
                code="unique",
            )

        user.set_password(validated_data["password"])
        user.save()

        return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "student_id", "email", "name", "password"]

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data["email"], name=validated_data["name"]
#         )
#         user.set_password(validated_data["password"])
#         user.save()
#         return user


class SignupViewset(generics.CreateAPIView):
    serializer_class = SignupSerializer
