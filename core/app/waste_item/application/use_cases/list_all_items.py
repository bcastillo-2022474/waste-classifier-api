from uuid import UUID

from core.app.waste_item.application.exceptions import UnableToSaveImageException, EmptyImageException
from core.app.waste_item.domain.entities import WasteItemInfo, Image, WasteItem
from core.app.waste_item.domain.ports import WasteItemRepository, ImageRepository

class ListAllItemsUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self):
        return self.waste_item_repository.list_all()
    