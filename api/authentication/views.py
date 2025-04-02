from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from api.authentication.adapters import UserRepositoryImplements
from core.app.user.application.use_cases.delete_user import DeleteUserUseCase
from core.app.user.application.use_cases.get_self_user import GetSelfUserUseCase
from api.utils import get_error_status_code_from_exception


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserApiView(APIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = DeleteUserUseCase(user_repository=repository) 
        try:
            user_id = str(request.user.id)
            use_case.execute(user_id)
            return Response({"message": "User deleted successfully"}, status=204)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data={"error": detail}, status=status_response)