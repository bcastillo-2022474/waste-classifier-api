from uuid import UUID

from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User
from core.app.user.application.exceptions import UserNotFoundException

class GetSelfUserUseCase:
    def __init__(self, user_repository:UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> User:
        user = self.user_repository.get_self_user(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        return user
        