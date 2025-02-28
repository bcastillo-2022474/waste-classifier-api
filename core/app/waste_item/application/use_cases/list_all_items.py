from core.app.waste_item.domain.ports import WasteItemRepository

class ListAllItemsUseCase:
    pass
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self):
        return self.waste_item_repository.list()
    