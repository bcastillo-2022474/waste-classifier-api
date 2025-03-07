from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFound

class DeleteUserUseCase:
    pass
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> None:
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFound
        self.user_repository.delete(user)

