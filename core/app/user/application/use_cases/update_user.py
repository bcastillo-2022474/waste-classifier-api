from uuid import UUID
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User
from core.app.user.application.exceptions import UserNotFoundException
from .dto import UpdateUserDTO
from pydantic import ValidationError

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, user_data: dict) -> User:
        user = self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundException("User not found")

        try:
            dto = UpdateUserDTO(**user_data)
        except ValidationError as e:
            raise ValueError(e.errors())

        # Usar setters de la entidad User (deben existir en la clase User)
        if dto.first_name is not None:
            user.set_first_name(dto.first_name)
        if dto.last_name is not None:
            user.set_last_name(dto.last_name)
        if dto.email is not None:
            user.set_email(dto.email)

        updated_user = self.user_repository.update(user)
        return updated_user