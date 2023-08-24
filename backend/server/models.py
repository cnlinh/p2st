from django.contrib.postgres.fields import ArrayField
from django.db import models
from enum import StrEnum
from pgvector.django import VectorField
from authuser.models import User


class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return f'{self.code} - {self.name}'

    class Meta:
        managed = False
        db_table = "modules"


class Enrollment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "enrollments"
        unique_together = (("user", "module"),)


class Topic(models.Model):
    id = models.BigAutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "topics"


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}. {self.user.student_id}: {self.topic.name}'

    class Meta:
        managed = False
        db_table = "conversations"


class Role(StrEnum):
    USER = "user"
    SYSTEM = "system"


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    embedding = VectorField(dimensions=512, blank=True, null=True)
    difficulty = models.FloatField()
    created_by = models.CharField(max_length=8)  # enum Role
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        if self.text is not None:
            return self.text[:75] + '...' if len(self.text) > 75 else self.text 
        return ''

    class Meta:
        managed = False
        db_table = "questions"


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        if self.text is not None:
            return self.text
        return ''

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
    
    def __str__(self):
        if self.text is not None:
            return f'{self.user.student_id}: {self.text}'
        return '{self.user}: '

    class Meta:
        managed = False
        db_table = "messages"


class Rating(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ratings"
        unique_together = (("message", "user"),)


class ExcludeFromCache(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    embedding = VectorField(dimensions=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        if self.text is not None:
            return self.text
        return ''

    class Meta:
        managed = False
        db_table = "exclude_from_cache"
