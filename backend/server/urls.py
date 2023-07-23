from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import signup, question, conversation

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("register", signup.SignupView.as_view(), name="register"),
    path("conversation", conversation.ConversationView.as_view(), name="conversation"),
]
