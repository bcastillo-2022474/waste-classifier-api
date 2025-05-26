from uuid import UUID
from core.app.user.application.exceptions import PasswordsDoNotMatchException, UserNotFoundException
from core.app.user.application.use_cases.dto import ChangePasswordDTO
from core.app.user.domain.ports import UserRepository
from authentication.models import User as UserModel

class ChangePasswordUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, passwords: ChangePasswordDTO):
        user_model = UserModel.objects.filter(id=user_id).first()
        if not user_model:
            raise UserNotFoundException(f"User not found with id: {user_id}")

        if not user_model.check_password(passwords.current_password):
            raise PasswordsDoNotMatchException("Passwords do not match")

        self.user_repository.update_password(user_id, passwords.new_password)
