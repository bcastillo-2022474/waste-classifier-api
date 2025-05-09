from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.exceptions import WasteItemNotFoundException

class GetOneItemByIdUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self, waste_item_id: str):
        item =  self.waste_item_repository.get(waste_item_id)
        if item is None:
            raise WasteItemNotFoundException()
         
        return item