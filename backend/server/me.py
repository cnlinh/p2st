from rest_framework import exceptions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Enrollment, Module
from authuser.models import User

class SelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["student_id", "email", "name"]

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["module"]

class SelfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        self_serializer = SelfSerializer(request.user)
        data = self_serializer.data

        if request.user.is_superuser:
            enrolled_modules = Module.objects.all().values_list("code", flat=True)
        else:
            enrolled_modules = Enrollment.objects.filter(student_id=request.user.student_id).values_list("module__code", flat=True)
        data["enrolled_modules"] = enrolled_modules
        return Response(data, status=status.HTTP_200_OK)

class ChangeIDSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=9, required=True)

class ChangeIDView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangeIDSerializer(data=request.data)

        if serializer.is_valid():
            new_student_id = request.data.get("student_id")
            if not new_student_id:
                raise exceptions.ValidationError("student id is required")

            if User.objects.filter(student_id=new_student_id).exists():
                raise exceptions.ValidationError("student id already exists")

            request.user.student_id = new_student_id
            request.user.save()
            return Response({"message": "student id updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
