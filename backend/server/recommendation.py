import os
import re
import openai
import numpy as np
import logging
from typing import Optional
import tensorflow_hub as hub

from django.db.models import QuerySet
from rest_framework import exceptions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Topic, Question

logger = logging.getLogger(__name__)

# One-time initialization
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"


class PopulateTopicView(APIView):
    permission_classes = [IsAuthenticated]
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def get(self, request, id):
        try:
            topic = Topic.objects.get(id=id)
        except Topic.DoesNotExist:
            return Response(
                {"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND
            )

        prompt = (
            f"What are some good questions to ask when learning about {topic.name}?"
        )
        questions = generate_questions(prompt)
        self.save_questions(id, questions)

        return Response({"data": questions}, status=status.HTTP_200_OK)

    def save_questions(self, topic_id, questions):
        topic = Topic.objects.get(id=topic_id)
        for question in questions:
            embeddings = generate_embedding(self.embedding_model, question)
            difficulty = 0.5
            Question.objects.create(
                topic=topic, text=question, embedding=embeddings, difficulty=difficulty
            )


def generate_embedding(embedding_model, text: str) -> np.ndarray:
    embeddings = embedding_model([text])[0].numpy()
    return embeddings.tolist()


def generate_questions(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    model_response = response["choices"][0]["message"]["content"]

    # Split the response into individual questions
    question_list = model_response.split("\n")

    # Use a regex to remove the number at the start of each question
    processed_questions_list = [
        re.sub("^\d+\.\s", "", question) for question in question_list if question
    ]

    return processed_questions_list
