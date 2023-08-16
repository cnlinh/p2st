from django.contrib.auth import password_validation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, exceptions
from authuser.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value: str) -> str:
        """
        Validate the new password against Django's password validation rules.
        """
        password_validation.validate_password(value)
        return value


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise exceptions.ValidationError("User with the provided email does not exist.")

            # Check current password
            if not check_password(current_password, user.password):
                raise exceptions.ValidationError("Current password is incorrect.")

            # Set and save the new password
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
