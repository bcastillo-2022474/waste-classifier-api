from rest_framework_simplejwt.views import TokenObtainPairView

from core.app.user.application.use_cases.signup import SignupUseCase
from core.app.user.domain.dtos import UserSignupDto
from .adapters import UserRepositoryImplements
from .serializers import CustomTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from api.utils import get_error_status_code_from_exception


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        use_case = SignupUseCase(user_repository=UserRepositoryImplements())

        try:
            response = use_case.execute(
                UserSignupDto(
                    first_name=request.data.get("first_name"),
                    last_name=request.data.get("last_name"),
                    email=request.data.get("email"),
                    password=request.data.get("password")
                )
            )
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)


class VerifyAuthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        return Response(request.user.to_entity(), status=status.HTTP_200_OK)
