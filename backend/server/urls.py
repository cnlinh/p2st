from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import signup, conversation, recommendation

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("register", signup.SignupView.as_view(), name="register"),
    path(
        "conversation/<int:id>",
        conversation.ConversationView.as_view(),
        name="conversation",
    ),
    path(
        "conversation",
        conversation.InitConversationView.as_view(),
        name="new_conversation",
    ),
    path(
        "topic/populate/<int:id>",
        recommendation.PopulateTopicView.as_view(),
        name="populate_topic",
    ),
    path("topics/all", topics.TopicView.as_view(), name="list_topic"),
    path(
        "recommendation/<int:id>",
        recommendation.QuestionsRecommendationView.as_view(),
        name="recommend_questions",
    ),
]
