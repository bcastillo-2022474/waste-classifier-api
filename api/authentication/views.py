from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
import json


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserApiView(APIView):
    print("UserApiView")