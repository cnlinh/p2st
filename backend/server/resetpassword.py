from django.contrib.auth import password_validation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, exceptions
from authuser.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password


class ResetPasswordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    student_id = serializers.CharField(max_length=9, required=True)
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value: str) -> str:
        """
        Validate the new password against Django's password validation rules.
        """
        password_validation.validate_password(value)
        return value


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            student_id = serializer.validated_data.get("student_id")
            email = serializer.validated_data.get("email")
            new_password = serializer.validated_data.get("new_password")

            try:
                user = User.objects.get(student_id=student_id)
            except User.DoesNotExist:
                raise exceptions.ValidationError("User with the provided student id does not exist.")

            # check all data matches
            if user.name != name or user.email != email:
                raise exceptions.ValidationError("Name and/or email does not match with record.")

            # Set and save the new password
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
