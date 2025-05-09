from datetime import datetime
from uuid import UUID

from core.app.waste_item.domain.ports import WasteItemRepository

class GetFrequencyRecyclingUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self, user_id: UUID, start_date: datetime, end_date: datetime):
        return self.waste_item_repository.get_frequency_recycling(user_id=user_id, start_date=start_date, end_date=end_date)