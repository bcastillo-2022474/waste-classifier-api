from django.urls import path
from .views import LoginView, UserApiView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("user", UserApiView.as_view(), name="crud_user"),
]

