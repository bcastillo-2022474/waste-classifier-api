import unittest
from unittest.mock import Mock

from core.app.waste_item.application.exceptions import EmptyImageError, UnableToProcessImageError
from core.app.waste_item.application.use_cases.scan_waste_item import ScanWasteItemUseCase
from core.app.waste_item.domain.entities import WasteItemInfo, WasteItemType, Image
from core.app.waste_item.domain.ports import ImageScannerRepository


class TestScanWasteItemUseCase(unittest.TestCase):
    def setUp(self):
        self.item_scanner_repository_mock = Mock(spec=ImageScannerRepository)


    def test_scan_waste_item(self):
        result_mock = WasteItemInfo(
            material="material",
            approximate_weight=1.0,
            type=WasteItemType.NON_RECYCLABLE,
        )

        self.item_scanner_repository_mock.scan.return_value = result_mock
        use_case = ScanWasteItemUseCase(item_scanner_repository=self.item_scanner_repository_mock)
        result = use_case.execute(image=Image(
            name="image.jpg",
            content_type="image/jpeg",
            size=100,
            content=b"content",
        ))

        self.assertEqual(result, result_mock)
        self.item_scanner_repository_mock.scan.assert_called_once()

    def test_scan_waste_item_with_empty_image(self):
        use_case = ScanWasteItemUseCase(item_scanner_repository=self.item_scanner_repository_mock)
        image_mock = Image(
            name="image.jpg",
            content_type="",
            size=0,
            content=b"",
        )


        with self.assertRaises(EmptyImageError):
            use_case.execute(image=image_mock)

        self.item_scanner_repository_mock.assert_not_called()



    def test_scan_waste_item_with_unable_to_process_image(self):
        use_case = ScanWasteItemUseCase(item_scanner_repository=self.item_scanner_repository_mock)
        image_mock = Image(
            name="image.jpg",
            content_type="image/jpeg",
            size=100,
            content=b"content",
        )
        self.item_scanner_repository_mock.scan.return_value = None

        self.item_scanner_repository_mock.scan.return_value = None

        with self.assertRaises(UnableToProcessImageError):
            use_case.execute(image=image_mock)

        self.item_scanner_repository_mock.scan.assert_called_once_with(image_mock)