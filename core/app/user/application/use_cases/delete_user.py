from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException
from uuid import UUID

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        
        self.user_repository.delete(user_id=user_id)
