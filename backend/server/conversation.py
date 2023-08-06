import os
import openai
import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub
from typing import List, TypedDict, Optional, NotRequired
from pgvector.django import CosineDistance

from django.contrib.auth import login, password_validation
from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import exceptions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Answer, Conversation, Message, Question, Role, ExcludeFromCache

logger = logging.getLogger(__name__)

# One-time initialization
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"
SIMILARITY_THRESHOLD = 0.775
GENERIC_QUESTIONS_SIMILARITY_THRESHOLD = 0.4


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "user"]

    def create(self, validated_data, **kwargs) -> Conversation:
        convo: Conversation
        try:
            convo = Conversation.objects.create(user=validated_data["user"])
        except Exception as e:
            raise exceptions.APIException(str(e))
        convo.save()
        return convo


class InitConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConversationSerializer(data={"user": request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    text = serializers.CharField(
        max_length=3000
    )  # gpt-3.5-turbo has max token limit of 4,096


def generate_embedding(embedding_model, text: str) -> np.ndarray:
    embeddings = embedding_model([text])[0].numpy()
    return embeddings


def find_similar_question(
    embeddings: np.ndarray, questions: QuerySet[Question]
) -> Optional[Question]:
    most_similar_question = (
        questions.annotate(distance=CosineDistance("embedding", embeddings))
        .order_by("distance")
        .first()
    )

    if most_similar_question is not None:
        similarity = 1 - most_similar_question.distance
        if similarity > SIMILARITY_THRESHOLD:
            logger.info(
                "found most similar question with similarity {}".format(similarity)
            )
            return most_similar_question
        return None

    return None


class ChatGPTMessage(TypedDict):
    id: NotRequired[int]
    role: str  # TO-DO: use Enum; user, system, assistant
    content: str


# TO-DO: cache messages of a conversation so we don't repeatedly call the DB
def get_conversation_messages(conversation_id: int) -> List[ChatGPTMessage]:
    messages = Message.objects.filter(conversation=conversation_id).order_by(
        "created_at"
    )
    return list(
        map(
            lambda m: ChatGPTMessage(
                id=m.id,
                role="user" if m.question is not None else "assistant",
                content=m.text,
            ),
            messages,
        )
    )


def generate_answer(
    conversation_id: int, past_messages: List[ChatGPTMessage], question: str
):
    messages = past_messages.copy()
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=list(
            map(lambda m: {"role": m["role"], "content": m["content"]}, messages)
        ),
        temperature=0,
        stream=True,  # server-sent events
    )

    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk["choices"][0]["delta"]  # extract the message
        collected_messages.append(chunk_message)  # save the message
        # print(f"Message received: {chunk_message}")  # print the delay and text

    full_reply_content = "".join([m.get("content", "") for m in collected_messages])
    # print(f"Full conversation received: {full_reply_content}")

    # TO-DO: Stream out responses as well to the user
    return full_reply_content


def fetch_answer(question_id: int) -> Answer:
    return Answer.objects.get(question=question_id)


def save_question(topic_id: int, text: str, embedding, created_by: Role) -> Question:
    qn: Question
    try:
        qn = Question.objects.create(
            topic_id=topic_id,
            text=text,
            embedding=embedding,
            difficulty=0.5,  # TO-DO
            created_by=created_by,
        )
    except Exception as e:
        raise exceptions.APIException(str(e))
    qn.save()
    return qn


def save_answer(question_id: int, response: str) -> Answer:
    ans: Answer
    try:
        ans = Answer.objects.create(
            question_id=question_id,
            text=response,
        )
    except Exception as e:
        raise exceptions.APIException(str(e))
    ans.save()
    return ans


def save_message(
    user_id: int,
    conversation_id: int,
    parent_message_id: Optional[int],
    question_id: Optional[int],
    answer_id: Optional[int],
    text: str,
) -> Message:
    msg: Message
    try:
        msg = Message.objects.create(
            user_id=user_id,
            conversation_id=conversation_id,
            parent_message_id=parent_message_id,
            question_id=question_id,
            answer_id=answer_id,
            text=text,
        )
    except Exception as e:
        raise exceptions.APIException(str(e))
    msg.save()
    return msg


def check_conversation_permissions(user_id: int, conversation_id: int):
    conversation = Conversation.objects.get(id=conversation_id)
    if conversation.user.id != user_id:
        raise exceptions.PermissionDenied(
            "User does not have permission to access this conversation"
        )


def is_generic_question(embedding: np.ndarray) -> bool:
    most_similar_question = (
        ExcludeFromCache.objects.annotate(
            distance=CosineDistance("embedding", embedding)
        )
        .order_by("distance")
        .first()
    )

    if most_similar_question is not None:
        similarity = 1 - most_similar_question.distance
        logger.debug(
            "most similar generic question: {}; {}".format(
                most_similar_question.text, similarity
            )
        )
        if similarity > GENERIC_QUESTIONS_SIMILARITY_THRESHOLD:
            logger.info("found generic question with similarity {}".format(similarity))
            # Should we add this question to ExcludeFromCache?
            # in order to continuously improve the system
            return True

    return False


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def get(self, request, id) -> Response:
        try:
            check_conversation_permissions(request.user.id, id)
            messages = get_conversation_messages(id)
            return Response(
                {
                    "messages": messages,
                    "latest_message_id": messages[-1]["id"]
                    if len(messages) > 0
                    else None,
                },
                status=status.HTTP_201_CREATED,
            )
        except exceptions.PermissionDenied as e:
            logger.error(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise exceptions.APIException("Internal server error")

    def post(self, request, id) -> Response:
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        question_text = serializer.validated_data["text"]
        topic_id = serializer.validated_data["topic_id"]
        try:
            check_conversation_permissions(request.user.id, id)

            past_messages = get_conversation_messages(id)
            # logger.debug("messages in conversation {}: {}".format(id, past_messages))

            parent_message = past_messages[-1]["id"] if len(past_messages) > 0 else None

            embeddings = generate_embedding(self.embedding_model, question_text)

            if not is_generic_question(embeddings):
                logger.debug("finding similar questions to '{}'".format(question_text))
                most_similar_question = find_similar_question(
                    embeddings, questions=Question.objects.all()
                )
                if most_similar_question is not None:
                    logger.info(
                        "found a similar question to '{}': question {}; '{}'".format(
                            question_text,
                            most_similar_question.id,
                            most_similar_question.text,
                        )
                    )
                    question_message = save_message(
                        request.user.id,
                        id,
                        parent_message,
                        most_similar_question.id,
                        None,
                        question_text,
                    )

                    response: str
                    try:
                        answer = fetch_answer(most_similar_question.id)
                        response = answer.text
                    except Answer.DoesNotExist:
                        # Must be a system-generated recommended question
                        response = generate_answer(id, past_messages, question_text)
                        logger.info(
                            "generated answer for question {}: {}".format(
                                most_similar_question.id, response
                            )
                        )
                        answer = save_answer(most_similar_question.id, response)

                    ans_msg = save_message(
                        request.user.id,
                        id,
                        question_message.id,
                        None,
                        answer.id,
                        response,
                    )
                    return Response(
                        {"data": response, "latest_message_id": ans_msg.id},
                        status=status.HTTP_201_CREATED,
                    )

            logger.info("new question asked: {}".format(question_text))
            question = save_question(
                topic_id, question_text, embeddings.tolist(), Role.USER
            )

            question_message = save_message(
                request.user.id,
                id,
                parent_message,
                question.id,
                None,
                question_text,
            )

            response = generate_answer(id, past_messages, question_text)
            # response = "This is a dummy response"
            logger.info(
                "generated answer for question {}: {}".format(question.id, response)
            )

            answer = save_answer(question.id, response)
            ans_msg = save_message(
                request.user.id, id, question_message.id, None, answer.id, response
            )

            return Response(
                {"answer": response, "latest_message_id": ans_msg.id},
                status=status.HTTP_201_CREATED,
            )
        except (exceptions.ValidationError, exceptions.PermissionDenied) as e:
            logger.error(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise exceptions.APIException("Internal server error")
