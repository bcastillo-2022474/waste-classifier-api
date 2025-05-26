from django.urls import path
from .views import UserAPIView, UserUpdateByIdAPIView, UserChangePasswordAPIView

urlpatterns = [
    path("user/self", UserAPIView.as_view(), name="user-self"),
    path("user/update/<uuid:user_id>", UserUpdateByIdAPIView.as_view(), name="update-user-by-id"),
    path("user/self/change-password", UserChangePasswordAPIView.as_view(), name="change-password"),
]