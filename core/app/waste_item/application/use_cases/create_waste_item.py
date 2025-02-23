from uuid import UUID

from core.app.waste_item.application.exceptions import UnableToSaveImageException, EmptyImageException
from core.app.waste_item.domain.entities import WasteItemInfo, Image, WasteItem
from core.app.waste_item.domain.ports import WasteItemRepository, ImageRepository


class CreateWasteItemUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository, image_repository: ImageRepository):
        self.waste_item_repository = waste_item_repository
        self.image_repository = image_repository

    def execute(self, waste_item: WasteItemInfo, image: Image, user_id: UUID) -> WasteItem:
        if image.size == 0:
            raise EmptyImageException("Image is empty")


        image_url = self.image_repository.save(image)
        if not image_url:
            raise UnableToSaveImageException("Error saving image")

        return self.waste_item_repository.create(WasteItem(
            type=waste_item.type,
            material=waste_item.material,
            approximate_weight=waste_item.approximate_weight,
            image=image_url,
            created_by_id=user_id,
            user_id=user_id
        ))