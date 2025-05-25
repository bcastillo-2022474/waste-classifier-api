from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException
import uuid

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> None:
        try:
            uuid_obj = uuid.UUID(user_id)
        except ValueError:
            raise ValueError(f"{user_id} is not a valid UUID")

        user = self.user_repository.get_by_id(uuid_obj)
        if user is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        
        self.user_repository.delete(uuid_obj)
