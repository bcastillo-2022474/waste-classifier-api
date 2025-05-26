from uuid import UUID
from core.app.user.application.exceptions import UserNotFoundException, UnauthorizedUserException
from core.app.user.application.use_cases.dto import ChangePasswordDTO
from core.app.user.domain.ports import UserRepository


class ChangePasswordUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, payload: ChangePasswordDTO):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id: {user_id} not found")

        if not self.user_repository.check_password(user_id=user_id, current_password=payload.current_password):
            raise UnauthorizedUserException("Passwords do not match")

        self.user_repository.update_password(user_id=user_id, new_password=payload.new_password)
