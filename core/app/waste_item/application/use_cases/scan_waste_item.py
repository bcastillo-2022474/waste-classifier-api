from core.app.waste_item.application.exceptions import EmptyImageException, UnableToProcessImageException
from core.app.waste_item.domain.ports import ImageScannerRepository
from core.app.waste_item.domain.entities import Image, WasteItemInfo

class ScanWasteItemUseCase:
    def __init__(self, item_scanner_repository: ImageScannerRepository):
        self.item_scanner_repository = item_scanner_repository

    def execute(self, image: Image) -> WasteItemInfo:
        if image.size == 0:
            raise EmptyImageException("Empty image")

        waste_item = self.item_scanner_repository.scan(image)
        if waste_item is None:
            raise UnableToProcessImageException("Unable to process image")
        return waste_item