from django.urls import path
from .views import UserAPIView

urlpatterns = [
    path("user/get_self_user", UserAPIView.as_view(), name="get_self_user"),
]