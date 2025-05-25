from uuid import uuid4, UUID

from core.app.user.domain.dtos import UserSignupDto
from core.app.user.domain.entities import User
from authentication.models import User as UserModel
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException


class UserRepositoryImplements(UserRepository):
    def create(self, user_dto: UserSignupDto) -> User:
        user = UserModel(
            email=user_dto.email,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
        )
        user.id = uuid4()
        user.set_password(user_dto.password)
        user.save()
        return user.to_entity()

    def list(self):
        return [user.to_entity() for user in UserModel.objects.all()]

    def get(self, user_id: UUID) -> User:
        user = UserModel.objects.filter(id=user_id).first()
        return user.to_entity() if user else None

    def get_by_email(self, email: str) -> User:
        user = UserModel.objects.filter(email=email).first()
        return user.to_entity() if user else None

    def update(self, user: User) -> User:
        user = UserModel.from_entity(entity=user)
        user.save(force_update=True)
        return user.to_entity()

    def delete(self, user_id: UUID):
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")

        user.delete()
