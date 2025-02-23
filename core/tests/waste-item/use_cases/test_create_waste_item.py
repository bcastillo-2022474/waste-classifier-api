import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from core.app.waste_item.application.exceptions import EmptyImageException, UnableToProcessImageException, \
    UnableToSaveImageException
from core.app.waste_item.application.use_cases.create_waste_item import CreateWasteItemUseCase
from core.app.waste_item.domain.entities import WasteItemInfo, WasteItemType, Image, WasteItem
from core.app.waste_item.domain.ports import WasteItemRepository, ImageRepository


class TestScanWasteItemUseCase(unittest.TestCase):
    def setUp(self):
        self.waste_item_repository = Mock(sepc=WasteItemRepository)
        self.image_repository = Mock(spec=ImageRepository)
        self.use_case = CreateWasteItemUseCase(
            waste_item_repository=self.waste_item_repository,
            image_repository=self.image_repository
        )


    def test_item_successfully_saved(self):
        image_id = uuid4()
        self.image_repository.save.return_value = image_id
        result_mock = WasteItem(
            type=WasteItemType.NON_RECYCLABLE,
            material="plastic",
            approximate_weight=1.5,
            image=image_id,
            created_by_id=uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=uuid4(),
            id=uuid4()
        )

        self.waste_item_repository.create.return_value = result_mock

        result = self.use_case.execute(
            waste_item=WasteItemInfo(
                type=WasteItemType.NON_RECYCLABLE,
                material="plastic",
                approximate_weight=1.5
            ),
            image=Image(
                name="image.jpg",
                content_type="image/jpeg",
                content=b"content",
                size=100
            ),
            user_id=uuid4(),
        )

        self.assertEqual(result, result_mock)
        self.image_repository.save.assert_called_once()
        self.waste_item_repository.create.assert_called_once()

    def test_item_saved_with_empty_image(self):
        with self.assertRaises(EmptyImageException):
            self.use_case.execute(
                waste_item=WasteItemInfo(
                    type=WasteItemType.NON_RECYCLABLE,
                    material="plastic",
                    approximate_weight=1.5
                ),
                image=Image(
                    name="image.jpg",
                    content_type="image/jpeg",
                    content=b"",
                    size=0
                ),
                user_id=uuid4(),
            )
        self.image_repository.save.assert_not_called()
        self.waste_item_repository.create.assert_not_called()


    def test_item_image_not_saved(self):
        self.image_repository.save.return_value = None
        with self.assertRaises(UnableToSaveImageException):
            self.use_case.execute(
                waste_item=WasteItemInfo(
                    type=WasteItemType.NON_RECYCLABLE,
                    material="plastic",
                    approximate_weight=1.5
                ),
                image=Image(
                    name="image.jpg",
                    content_type="image/jpeg",
                    content=b"content",
                    size=100
                ),
                user_id=uuid4(),
            )

        self.image_repository.save.assert_called_once()
        self.waste_item_repository.create.assert_not_called()