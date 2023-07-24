import os
import openai
from typing import List, TypedDict, Optional

from django.contrib.auth import login, password_validation
from django.shortcuts import render
from rest_framework import exceptions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, Message, Question

openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"


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


class InitConversationView(APIView):
    def post(self, request):
        serializer = ConversationSerializer(data={})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ["embedding", "difficulty"]

    # validate text length

    def create(self, validated_data, **kwargs) -> Question:
        qn: Question
        try:
            qn = Question.objects.create(
                topic=None,  # TO-DO
                text=validated_data["text"],
                embedding=None,  # TO-DO
                difficulty=0.5,  # TO-DO
            )
        except Exception as e:
            raise exceptions.APIException(str(e))
        qn.save()
        return qn


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    # validate text length

    def create(self, validated_data, **kwargs) -> Message:
        msg: Message
        try:
            msg = Message.objects.create(
                user=validated_data["user"],
                conversation=validated_data["conversation"],
                parent_message=validated_data["parent_message"],
                question=validated_data["question"],
                answer=validated_data["answer"],
                text=validated_data["text"],
            )
        except Exception as e:
            raise exceptions.APIException(str(e))
        msg.save()
        return msg


class ChatGPTMessage(TypedDict):
    id: Optional[int]
    role: str  # TO-DO: use Enum; user, system, assistant
    content: str


# TO-DO: cache messages of a conversation so we don't repeatedly call the DB
def get_conversation_messages(conversation_id: int) -> List[ChatGPTMessage]:
    return []


def generate_answer(
    conversation_id: int, past_messages: List[ChatGPTMessage], question: str
):
    messages = past_messages.copy()
    messages.append({"id": 1, "role": "user", "content": question})
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
        print(f"Message received: {chunk_message}")  # print the delay and text

    full_reply_content = "".join([m.get("content", "") for m in collected_messages])
    print(f"Full conversation received: {full_reply_content}")

    # TO-DO: Stream out responses as well to the user
    return full_reply_content


class ConversationView(APIView):
    def post(self, request, id):
        print(id)
        qn_serializer = QuestionSerializer(data={"text": request.data["text"]})
        if qn_serializer.is_valid():
            # 1. embed question
            # 2. if existing, get answer from db
            # 3. else, call chatgpt API to generate answer

            # new question:
            try:
                qn_serializer.save()
                past_messages = get_conversation_messages(id)
                parent_message = (
                    past_messages[-1].id if len(past_messages) > 0 else None
                )
                msg_serializer = MessageSerializer(
                    data={
                        "user": request.user.id,
                        "conversation": id,
                        "parent_message": parent_message,
                        "question": None,
                        "answer": None,
                        "text": request.data["text"],
                    }
                )
                response = generate_answer(id, past_messages, request.data["text"])

                return Response({"data": response}, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise exceptions.APIException(str(e))
        return Response(qn_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
