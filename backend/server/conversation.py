from django.contrib.auth import login, password_validation
from django.shortcuts import render
from rest_framework import exceptions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id"]

    def create(self, validated_data, **kwargs) -> Conversation:
        convo: Conversation
        try:
            convo = Conversation.objects.create()
        except Exception as e:
            raise exceptions.APIException(str(e))
        convo.save()
        return convo


class ConversationView(APIView):
    def post(self, request):
        serializer = ConversationSerializer(data={})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
