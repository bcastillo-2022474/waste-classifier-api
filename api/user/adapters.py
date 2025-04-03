from uuid import uuid4, UUID

from core.app.user.domain.entities import User
from authentication.models import User as UserModel
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException

class UserRepositoryImplements(UserRepository):

  def get_self_user(self, user_id: UUID) -> User:
    user = UserModel.objects.filter(id=user_id).first()
    return user.to_entity() if user else None
  
  