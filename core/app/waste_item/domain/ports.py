from typing import Protocol

from .entities import WasteItemInfo, Image

class ImageScannerRepository(Protocol):
    def scan(self, image: Image) -> WasteItemInfo: ...