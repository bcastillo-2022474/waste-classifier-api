from uuid import UUID
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User
from core.app.user.application.exceptions import UserNotFoundException

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, user_data: dict) -> User:
        user = self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        for field in ["first_name", "last_name", "email"]:
            if field in user_data:
                setattr(user, field, user_data[field])

        updated_user = self.user_repository.update(user)
        return updated_user