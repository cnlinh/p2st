from django.contrib import admin

from .models import (
    Module, Enrollment, Topic, Conversation, 
    Question, Answer, Message, Rating
)

admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Topic)
admin.site.register(Conversation)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Message)
admin.site.register(Rating)