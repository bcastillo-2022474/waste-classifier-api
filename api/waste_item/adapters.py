import random

from core.app.waste_item.domain.ports import ImageScannerRepository
from core.app.waste_item.domain.entities import WasteItemInfo, Image


class ImageScannerRepositoryImpl(ImageScannerRepository):
    def scan(self, image: Image) -> WasteItemInfo:
        # randomized mocked data
        possible_materials = ["plastic", "paper", "glass", "metal", "organic"]
        possible_types = ["non_recyclable", "recyclable", "organic"]

        return WasteItemInfo(
            material=random.choice(possible_materials),
            type=random.choice(possible_types),
            approximate_weight=random.uniform(0.1, 10.0)
        )

