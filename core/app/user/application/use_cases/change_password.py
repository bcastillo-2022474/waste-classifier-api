from uuid import UUID
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException

class ChangePasswordUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, new_password: str):
        user = self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundException("User not found with id: {user_id}")
        self.user_repository.update_password(user_id, new_password)