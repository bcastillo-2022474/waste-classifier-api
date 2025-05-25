from core.app.user.domain.dtos import UserSignupDto
from core.app.user.domain.entities import User
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserAlreadyExists, UnableToCreateUser


class SignupUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_dto: UserSignupDto) -> User:
        foundUser = self.user_repository.get_by_email(email=user_dto.email)
        if foundUser:
            raise UserAlreadyExists(f"User with email {user_dto.email} already exists")

        user = self.user_repository.create(user=user_dto)

        if not user:
            raise UnableToCreateUser(f"Unable to create user with email {user_dto.email}")

        return user
