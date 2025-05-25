from uuid import UUID
from core.app.user.application.use_cases.dto import ChangePasswordDTO
from core.app.user.domain.ports import UserRepository

class ChangePasswordUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, passwords: ChangePasswordDTO):
        
        if not passwords.current_password or not passwords.new_password:
            raise ValueError("Current password and new password must be provided")
        
        self.user_repository.update_password(user_id, passwords)