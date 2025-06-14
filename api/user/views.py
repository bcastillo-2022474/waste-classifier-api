from api.authentication.adapters import UserRepositoryImplements
from core.app.user.application.use_cases.dto import ChangePasswordDTO, UpdateUserDTO
from core.app.user.application.use_cases.get_self_user import GetSelfUserUseCase
from core.app.user.application.use_cases.delete_user import DeleteUserUseCase
from core.app.user.application.use_cases.update_user import UpdateUserUseCase
from core.app.user.application.use_cases.change_password import ChangePasswordUseCase

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
            user = use_case.execute(user_id=request.user.id)
            return Response(user, status=status.HTTP_200_OK)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)

    @staticmethod
    def delete(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = DeleteUserUseCase(user_repository=repository)
        try:
            use_case.execute(user_id=request.user.id)
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)

    @staticmethod
    def put(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = UpdateUserUseCase(user_repository=repository)
        try:
            user_id = request.user.id
            user_data = request.data
            updated_user = use_case.execute(user_id, UpdateUserDTO(
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                email=user_data.get("email")
            ))
            return Response(updated_user, status=200)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)

class UserChangePasswordAPIView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = ChangePasswordUseCase(user_repository=repository)
        try:
            user_id = request.user.id
            use_case.execute(user_id, ChangePasswordDTO(
                current_password=request.data.get("current_password"),
                new_password=request.data.get("new_password")
            ))
            return Response({"message": "Password updated successfully"}, status=200)
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
            updated_user = use_case.execute(user_id, UpdateUserDTO(
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                email=user_data.get("email")
            ))
            return Response(updated_user, status=200)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data=detail, status=status_response)
