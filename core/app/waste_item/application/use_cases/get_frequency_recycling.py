from datetime import datetime
from uuid import UUID

from core.app.user.application.exceptions import UserNotFoundException
from core.app.user.domain.ports import UserRepository
from core.app.waste_item.domain.ports import WasteItemRepository

class GetFrequencyRecyclingUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository, user_repository: UserRepository):
        self.waste_item_repository = waste_item_repository
        self.user_repository = user_repository

    def execute(self, user_id: UUID, start_date: datetime, end_date: datetime):
        user = self.user_repository.get(user_id=user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} was not found")

        return self.waste_item_repository.get_frequency_recycling(user_id=user_id, start_date=start_date, end_date=end_date)