from typing import List
from core.app.waste_item.domain.entities import WasteItem
from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.exceptions import UserNotFoundException

class GetItemsByUserIdUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self, user_id: str) -> List[WasteItem]:
        if not self.waste_item_repository.user_exists(user_id):
            raise UserNotFoundException()
        
        return self.waste_item_repository.list_by_user_id(user_id)
