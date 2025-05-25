from core.app.user.application.use_cases.dto import UpdateUserDTO
from user.adapters import UserRepositoryImplements
from core.app.user.application.use_cases.get_self_user import GetSelfUserUseCase
from core.app.user.application.use_cases.delete_user import DeleteUserUseCase
from core.app.user.application.use_cases.update_user import UpdateUserUseCase

from rest_framework.response import Response
from api.utils import get_error_status_code_from_exception
from rest_framework.views import APIView

class UserAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        repository = UserRepositoryImplements()
        use_case = GetSelfUserUseCase(user_repository=repository) 
        try:
            user_id = str(request.user.id)
            user = use_case.execute(user_id)
            return Response({"user": user}, status=200)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(data={"error": detail}, status=status_response)
        
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
