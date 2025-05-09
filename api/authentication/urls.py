from django.urls import path
from .views import LoginView, VerifyAuthView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/verify", VerifyAuthView.as_view(), name="verify")
]
