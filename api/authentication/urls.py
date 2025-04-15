from django.urls import path
from .views import LoginView, VerifyAuthView, UserApiView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/verify", VerifyAuthView.as_view(), name="verify"),
    path("user", UserApiView.as_view(), name="crud_user"),
]

