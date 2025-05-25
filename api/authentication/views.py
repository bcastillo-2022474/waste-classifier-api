from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyAuthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        return Response(request.user.to_entity(), status=status.HTTP_200_OK)
