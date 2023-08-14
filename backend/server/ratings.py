import os
import re
import openai
import numpy as np
import logging
from typing import Optional, List
import tensorflow_hub as hub
from pgvector.django import CosineDistance

from django.db import transaction, IntegrityError
from django.db.models import QuerySet
from django.db.models.query import RawQuerySet
from rest_framework import exceptions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Rating

from . import conversation

logger = logging.getLogger(__name__)


class CreateRatingSerializer(serializers.Serializer):
    score = serializers.IntegerField()


class RatingsView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, id):
        message_id = id
        serializer = CreateRatingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            prev_rating = get_rating(message_id, request.user.id)
            if prev_rating.score == serializer.validated_data["score"]:
                return Response({"id": prev_rating.id}, status=status.HTTP_200_OK)
            # if rating exists, delete it
            delete_rating(message_id, request.user.id)
        except Rating.DoesNotExist:
            pass
        except Exception as e:
            logger.error(e)
            raise exceptions.APIException("Internal server error")

        try:
            rating = save_rating(
                message_id, request.user.id, serializer.validated_data["score"]
            )
            return Response({"id": rating.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            raise exceptions.APIException("Internal server error")

    def get(self, request, id):
        message_id = id
        try:
            rating = get_rating(message_id, request.user.id)
            return Response(
                {"id": rating.id, "score": rating.score}, status=status.HTTP_200_OK
            )
        except Rating.DoesNotExist:
            return Response(
                {"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(e)
            raise exceptions.APIException("Internal server error")


def get_rating(message_id: int, user_id: int) -> Rating:
    return Rating.objects.get(message_id=message_id, user_id=user_id)


def delete_rating(message_id: int, user_id: int):
    logger.info("Deleting rating for message {} by user {}".format(message_id, user_id))
    return Rating.objects.filter(message_id=message_id, user_id=user_id).delete()


def save_rating(message_id: int, user_id: int, score: int) -> Rating:
    logger.info("Saving rating for message {} by user {}".format(message_id, user_id))
    rating = Rating(message_id=message_id, user_id=user_id, score=score)
    rating.save()
    return rating
