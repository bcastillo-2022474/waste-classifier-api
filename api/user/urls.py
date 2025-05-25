from django.urls import path
from .views import UserAPIView, UserUpdateByIdAPIView

urlpatterns = [
    path("user/get-self-user", UserAPIView.as_view(), name="get-self-user"),
    path("user/self", UserAPIView.as_view(), name="update-user"),
    path("user/update/<uuid:user_id>", UserUpdateByIdAPIView.as_view(), name="update-user-by-id"),
    path("user/change-password", UserAPIView.as_view(), name="change-password"),
]