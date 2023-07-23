from django.contrib import admin

from .models import Topic, Conversation, Question, Message, Answer, Recommendation

admin.site.register(Topic)
admin.site.register(Conversation)
admin.site.register(Question)
admin.site.register(Message)
admin.site.register(Answer)
admin.site.register(Recommendation)
