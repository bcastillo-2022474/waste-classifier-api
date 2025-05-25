from django.urls import path
from .views import UserAPIView

urlpatterns = [
    path("user/self", UserAPIView.as_view(), name="get-self-user")
]