from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from api.authentication.adapters import UserRepositoryImplements
from core.app.user.application.use_cases.delete_user import DeleteUserUseCase
from api.utils import get_error_status_code_from_exception
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


class UserApiView(APIView):

    @staticmethod
    def delete(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = DeleteUserUseCase(user_repository=repository)

        try:
            user_id = str(request.user.id)
            use_case.execute(user_id)
            return Response(
                {"message": "User deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data={"error": detail}, status=status_response)
