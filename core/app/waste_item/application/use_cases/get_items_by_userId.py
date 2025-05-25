from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.exceptions import WasteItemNotFoundException

class GetItemsByUserIdUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self, user_id: str):
        items = self.waste_item_repository.list_by_user_id(user_id)
        if not items:
            raise WasteItemNotFoundException()
        
        return items