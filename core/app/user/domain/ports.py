from typing import Protocol
from uuid import UUID

from core.app.user.application.use_cases.dto import ChangePasswordDTO

from .dtos import UserSignupDto
from .entities import User

class UserRepository(Protocol):
    def create(self, user_dto: UserSignupDto) -> User | None: ...
    def get(self, user_id: UUID) -> User | None: ...
    def list(self) -> list[User]: ...
    def delete(self, user_id: UUID) -> None: ...
    def update(self, user: User) -> User: ...
    def get_by_email(self, email: str) -> User | None: ...
    def update_password(self, user_id: UUID, new_password: str) -> None: ...
    def get_by_id(self, user_id: UUID) -> User | None: ...
    def check_password(self, user_id: UUID, current_password: str) -> bool: ...
