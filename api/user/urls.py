from django.urls import path
from .views import UserAPIView

urlpatterns = [
    path("user/get-self-user", UserAPIView.as_view(), name="get-self-user")
]