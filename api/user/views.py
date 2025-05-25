from api.authentication.adapters import UserRepositoryImplements
from core.app.user.application.use_cases.get_self_user import GetSelfUserUseCase
from core.app.user.application.use_cases.delete_user import DeleteUserUseCase
from core.app.user.application.use_cases.update_user import UpdateUserUseCase

from rest_framework.response import Response
from api.utils import get_error_status_code_from_exception
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = GetSelfUserUseCase(user_repository=repository)
        try:
            user_id = str(request.user.id)
            user = use_case.execute(user_id)
            return Response(user, status=status.HTTP_200_OK)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)

    @staticmethod
    def delete(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = DeleteUserUseCase(user_repository=repository)
        try:
            user_id = str(request.user.id)
            use_case.execute(user_id)
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data={"error": detail}, status=status_response)

    @staticmethod
    def put(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = UpdateUserUseCase(user_repository=repository)
        try:
            user_id = request.user.id
            user_data = request.data
            updated_user = use_case.execute(user_id, user_data)
            return Response(updated_user, status=200)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)

class UserUpdateByIdAPIView(APIView):
    @staticmethod
    def put(request, user_id, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = UpdateUserUseCase(user_repository=repository)
        try:
            user_data = request.data
            updated_user = use_case.execute(user_id, user_data)
            return Response(updated_user, status=200)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)
