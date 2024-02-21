import os
import re
import openai
import numpy as np
import logging
from typing import Optional, List
import tensorflow_hub as hub
from pgvector.django import CosineDistance

from django.db.models import QuerySet
from django.db.models.query import RawQuerySet
from rest_framework import exceptions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Topic, Message, Question, Role

from . import conversation

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


class QuestionsRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def get(self, request, id):
        parent_messages = get_k_parent_messages(id, 5)
        response = generate_follow_up_questions(
            list(
                map(
                    lambda m: conversation.ChatGPTMessage(
                        id=m.id,
                        role="user" if m.question is not None else "assistant",
                        content=m.text,
                    ),
                    parent_messages,
                )
            )
        )

        qn: Message
        for i in range(len(parent_messages) - 1, -1, -1):
            msg = parent_messages[i]
            if msg.question is not None:
                qn = msg
                break
        logger.debug(f"parent question: {qn}")
        if qn is None:
            logger.error("parent question not found")
            raise exceptions.APIException("Internal server error")
        for question in response:
            embeddings = generate_embedding(self.embedding_model, question)
            #conversation.save_question(
            #    qn.question.topic_id, question, embeddings, Role.SYSTEM
            #)
        # TO-DO: Incorporate existing questions to recommend questions
        find_similar_questions(qn.question.topic_id, qn.question.embedding)

        return Response({"data": response}, status=status.HTTP_201_CREATED)


def find_similar_questions(topic_id: int, embeddings: np.ndarray) -> Optional[Question]:
    annotated_questions = (
        Question.objects.filter(topic_id=topic_id)
        .annotate(distance=CosineDistance("embedding", embeddings))
        .order_by("distance")
        .all()
    )

    for question in annotated_questions:
        print(question.text, 1 - question.distance)

    return None


MESSAGE_TRAVERSAL_QUERY = """WITH RECURSIVE RecursiveCTE AS (
    -- Anchor member: Select the child node
    SELECT id, text, parent_message_id, question_id, answer_id, 0 AS level
    FROM messages
    WHERE id = {}

    UNION ALL

    -- Recursive member: Join the CTE with the table to find the parent node
    SELECT m.id, m.text, m.parent_message_id, m.question_id, m.answer_id, rc.level + 1
    FROM messages m
    INNER JOIN RecursiveCTE rc ON m.id = rc.parent_message_id
    WHERE rc.level < {}
)
-- Query the RecursiveCTE to get the results in reverse order (from child to root)
SELECT id, text, parent_message_id, question_id, answer_id, level
FROM RecursiveCTE
ORDER BY level DESC;"""


def get_k_parent_messages(src_message_id: int, k: int) -> RawQuerySet:
    return Message.objects.raw(MESSAGE_TRAVERSAL_QUERY.format(src_message_id, k))


def generate_follow_up_questions(past_messages):
    messages = past_messages.copy()
    messages.append(
        {
            "id": None,
            "role": "user",
            "content": "please provide a list of three follow-up questions for our current conversation without any introduction",
        }
    )

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=list(
            map(lambda m: {"role": m["role"], "content": m["content"]}, messages)
        ),
        temperature=0,
        stream=False,
    )
    model_response = response["choices"][0]["message"]["content"]

    # Split the response into individual questions
    question_list = model_response.split("\n")

    # Use a regex to remove the number at the start of each question
    processed_questions_list = [
        re.sub("^\d+\.\s", "", question) for question in question_list if question
    ]
    return processed_questions_list
