from uuid import UUID
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User
from core.app.user.application.exceptions import UserNotFoundException
from .dto import UpdateUserDTO

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, user_data: UpdateUserDTO) -> User:
        user = self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundException("User not found with id: {user_id}")

        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        if user_data.email is not None:
            user.email = user_data.email

        updated_user = self.user_repository.update(user)
        return updated_user