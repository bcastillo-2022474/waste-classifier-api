from uuid import uuid4, UUID

from core.app.user.domain.dtos import UserSignupDto
from core.app.user.domain.entities import User
from authentication.models import User as UserModel
from core.app.user.domain.ports import UserRepository


class UserRepositoryImplements(UserRepository):
    def create(self, user_dto: UserSignupDto) -> User:
        user = UserModel(
            email=user_dto.email,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            is_active=True,
        )
        user.id = uuid4()
        user.set_password(user_dto.password)
        user.save()
        return user.to_entity()

    def list(self):
        return [user.to_entity() for user in UserModel.objects.filter(is_active=True)]

    def get(self, user_id: UUID) -> User:
        user = UserModel.objects.filter(id=user_id).first()
        return user.to_entity() if (user and user.is_active) else None

    def get_by_email(self, email: str) -> User:
        user = UserModel.objects.filter(email=email).first()
        return user.to_entity() if (user and user.is_active) else None

    def update(self, user: User) -> User:
        user = UserModel.from_entity(entity=user)
        user.save(force_update=True)
        return user.to_entity()

    def delete(self, user_id: UUID):
        user = UserModel.objects.filter(id=user_id).first()
        user.is_active = False
        user.save()

    def get_by_id(self, user_id: UUID) -> User:
        user = UserModel.objects.filter(id=user_id).first()
        return user.to_entity() if (user and user.is_active) else None

    def update_password(self, user_id: UUID, new_password: str):
        user = UserModel.objects.filter(id=user_id).first()
        user.set_password(new_password)
        user.save()

    def check_password(self, user_id: UUID, current_password: str) -> bool:
        user = UserModel.objects.filter(id=user_id).first()
        return user.check_password(current_password)