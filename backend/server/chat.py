from django.contrib.auth import login, password_validation
from django.shortcuts import render
from rest_framework import exceptions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from authuser.models import User


class ChatService:
    pass


class ChatSerializer(serializers.Serializer):
    def create(self, validated_data, **kwargs):
        pass


class ChatView(APIView):
    def post(self, request):
        # used for validating and deserializing input, and for serializing output
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
