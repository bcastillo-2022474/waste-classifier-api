from core.app.waste_item.domain.ports import WasteItemRepository

class GetObjetsRecyclingMaterialUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self, material_waste: str):
        if not material_waste:
            raise ValueError("El material no puede estar vacío.")

        item = self.waste_item_repository.getMaterial(material_waste)
        if item is None:
            return None

        return {"material": item.material, "count": item.count}