from uuid import uuid4, UUID

from core.app.user.domain.entities import User
from authentication.models import User as UserModel
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException

class UserRepositoryImplements(UserRepository): 
    
    def find_by_id(self, user_id: UUID) -> User:
        user = UserModel.objects.filter(id=user_id).first()
        return user.to_entity() if user else None
    
    def list(self):
        return [user.to_entity() for user in UserModel.objects.all()]
    
    def get(self, user_id: UUID) -> User:
        return UserModel.objects.get(id=user_id).to_entity()
    
    def get_by_username(self, username: str) -> User:
        return UserModel.objects.get(username=username).to_entity()

    def get_by_email(self, email: str) -> User:
        return UserModel.objects.get(email=email).to_entity()

    def update(self, user: User) -> User:
        user = UserModel.from_entity(entity=user)
        user.save(force_update=True)
        return user.to_entity()

    def delete(self, user_id: UUID):
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        user.delete()

    def exists(self, user_id: UUID) -> bool:
        return UserModel.objects.filter(id=user_id).exists()

    def exists_by_username(self, username: str) -> bool:
        return UserModel.objects.filter(username=username).exists()

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

