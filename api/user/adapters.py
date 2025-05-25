from uuid import UUID

from core.app.user.domain.entities import User
from authentication.models import User as UserModel
from core.app.user.domain.ports import UserRepository
from core.app.user.application.exceptions import UserNotFoundException

class UserRepositoryImplements(UserRepository):

  def get(self, user_id: UUID) -> User:
    user = UserModel.objects.filter(id=user_id).first()
    return user.to_entity() if user else None
  
  def update(self, user: User) -> User:
      user_model = UserModel.objects.filter(id=user.id).first()
      if not user_model:
          raise UserNotFoundException("User not found")
      # Actualiza los campos permitidos
      user_model.first_name = user.first_name
      user_model.last_name = user.last_name
      user_model.email = user.email
      user_model.save()
      return user_model.to_entity()