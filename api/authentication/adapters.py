from uuid import uuid4, UUID

from core.app.user.domain.entities import User
from authentication.models import User as UserModel
from core.app.user.domain.ports import UserRepository

class UserRepositoryImplements(UserRepository): 
    
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
        UserModel.objects.get(id=user_id).delete()

    def exists(self, user_id: UUID) -> bool:
        return UserModel.objects.filter(id=user_id).exists()

    def exists_by_username(self, username: str) -> bool:
        return UserModel.objects.filter(username=username).exists()

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

