from core.app.waste_item.domain.ports import WasteItemRepository

class GetAllRecyclingMaterialUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self):
        return self.waste_item_repository.get_all_material_count()
         