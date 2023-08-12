from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import signup, conversation, recommendation, ratings, modules

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("register", signup.SignupView.as_view(), name="register"),
    path(
        "conversations/<int:id>",
        conversation.ConversationView.as_view(),
        name="conversation",
    ),
    path(
        "conversations",
        conversation.ConversationsView.as_view(),
        name="conversations",
    ),
    path(
        "topics/populate/<int:id>",
        recommendation.PopulateTopicView.as_view(),
        name="populate_topic",
    ),
    path("topics", modules.TopicView.as_view(), name="topics"),
    path(
        "recommendations/<int:id>",
        recommendation.QuestionsRecommendationView.as_view(),
        name="recommend_questions",
    ),
    path(
        "ratings/<int:id>",
        ratings.RatingsView.as_view(),
        name="ratings",
    ),
]
