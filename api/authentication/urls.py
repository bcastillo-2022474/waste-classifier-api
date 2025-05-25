from django.urls import path
from .views import LoginView, VerifyAuthView, SignupView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/signup", SignupView.as_view(), name="signup"),
    path("auth/verify", VerifyAuthView.as_view(), name="verify")
]
