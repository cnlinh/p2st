from django.contrib.postgres.fields import ArrayField
from django.db import models
from authuser.models import User


class Topic(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "topics"


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "conversations"


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    embedding = ArrayField(models.FloatField(blank=True, null=True))
    difficulty = models.FloatField()

    class Meta:
        managed = False
        db_table = "questions"


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    quality = models.IntegerField(blank=True, null=True)
    relevance = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "answers"


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    parent_message = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "messages"


class Recommendation(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    hit = models.BooleanField(blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True)
    relevance = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "recommendations"
