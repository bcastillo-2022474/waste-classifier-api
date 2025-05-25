from uuid import UUID

from core.app.user.domain.dtos import UserSignupDto
from core.app.user.domain.entities import User
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserAlreadyExists, UnableToCreateUser


class SignupUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str, first_name: str, last_name: str) -> User:
        foundUser = self.user_repository.get_by_email(email=email)
        if foundUser:
            raise UserAlreadyExists(f"User with email {email} already exists")

        user = self.user_repository.create(UserSignupDto(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        ))

        if not user:
            raise UnableToCreateUser(f"Unable to create user with email {email}")

        return user
