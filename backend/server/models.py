# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from authuser.models import User


class Topic(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "topics"


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "conversations"


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topic, models.DO_NOTHING, blank=True, null=True)
    text = models.TextField()
    embedding = models.TextField(blank=True, null=True)  # This field type is a guess.
    difficulty = models.FloatField()

    class Meta:
        managed = False
        db_table = "questions"


class UserQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    question = models.ForeignKey(Question, models.DO_NOTHING)
    conversation = models.ForeignKey(Conversation, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    parent_question = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "user_questions"
        unique_together = (("user", "question", "parent_question"),)


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_question = models.ForeignKey(UserQuestion, models.DO_NOTHING)
    text = models.TextField()
    quality = models.IntegerField(blank=True, null=True)
    relevance = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "answers"


class Recommendation(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_question = models.ForeignKey(UserQuestion, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    hit = models.BooleanField(blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True)
    relevance = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "recommendations"
