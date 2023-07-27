import os
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub
from typing import List, TypedDict, Optional

from django.contrib.auth import login, password_validation
from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import exceptions, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Answer, Conversation, Message, Question

# One-time initialization
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"
SIMILARITY_THRESHOLD = 0.775


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
                embedding=validated_data["embeddings"],  # TO-DO
                difficulty=0.5,  # TO-DO
            )
        except Exception as e:
            raise exceptions.APIException(str(e))
        qn.save()
        return qn


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

    def create(self, validated_data, **kwargs) -> Answer:
        ans: Answer
        try:
            ans = Answer.objects.create(
                question=validated_data["question"],
                text=validated_data["text"],
            )
        except Exception as e:
            raise exceptions.APIException(str(e))
        ans.save()
        return ans


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


def generate_embedding(embedding_model, text: str) -> np.ndarray:
    embeddings = embedding_model([text])[0].numpy()
    return embeddings


def find_similar(embeddings: np.ndarray, questions) -> Optional[Question]:
    most_similar_question = None
    max_similarity = 0

    for question in questions:
        # TO-DO: store embeddings as np array in DB?
        similarity = cosine_similarity([embeddings], [np.array(question.embedding)])[0][
            0
        ]
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = question

    return most_similar_question


class ChatGPTMessage(TypedDict):
    id: Optional[int]
    role: str  # TO-DO: use Enum; user, system, assistant
    content: str


# TO-DO: cache messages of a conversation so we don't repeatedly call the DB
def get_conversation_messages(
    conversations: QuerySet[Message], conversation_id: int
) -> List[ChatGPTMessage]:
    messages = conversations.filter(conversation=conversation_id).order_by("created_at")
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
    messages.append({"id": None, "role": "user", "content": question})
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


def save_question(text: str, embeddings) -> Question:
    qn_serializer = QuestionSerializer(data={"text": text})
    qn_serializer.is_valid(raise_exception=True)
    return qn_serializer.save(embeddings=embeddings)


def save_answer(question_id: int, response: str) -> Answer:
    ans_serializer = AnswerSerializer(data={"question": question_id, "text": response})
    ans_serializer.is_valid(raise_exception=True)
    return ans_serializer.save()


def save_message(
    user_id: int,
    conversation_id: int,
    parent_message_id: Optional[int],
    question_id: Optional[int],
    answer_id: Optional[int],
    text: str,
) -> Message:
    msg_serializer = MessageSerializer(
        data={
            "user": user_id,
            "conversation": conversation_id,
            "parent_message": parent_message_id,
            "question": question_id,
            "answer": answer_id,
            "text": text,
        }
    )
    msg_serializer.is_valid(raise_exception=True)
    return msg_serializer.save()


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def post(self, request, id):
        # 1. embed question
        embeddings = generate_embedding(self.embedding_model, request.data["text"])
        # 2. if existing, get answer from db
        # most_similar_question = find_similar(
        #     embeddings, questions=Question.objects.all()
        # )
        # if most_similar_question is not None:
        #     # dont regenerate answer
        #     return Response(
        #         {"data": "Similar to question" + str(most_similar_question)},
        #         status=status.HTTP_201_CREATED,
        #     )
        # 3. else, call chatgpt API to generate answer

        # new question:
        qn = save_question(request.data["text"], embeddings.tolist())

        try:
            past_messages = get_conversation_messages(Message.objects.all(), id)

            parent_message = past_messages[-1]["id"] if len(past_messages) > 0 else None

            qn_msg = save_message(
                request.user.id,
                id,
                parent_message,
                qn.id,
                None,
                request.data["text"],
            )

            # skip to save money :)
            response = generate_answer(id, past_messages, request.data["text"])
            # response = "This is a dummy response"

            ans = save_answer(qn.id, response)
            ans_msg = save_message(
                request.user.id, id, qn_msg.id, None, ans.id, response
            )

            return Response({"data": response}, status=status.HTTP_201_CREATED)
        except exceptions.ValidationError as e:
            raise e
        except Exception as e:
            print(e)
            raise exceptions.APIException("Internal server error")
