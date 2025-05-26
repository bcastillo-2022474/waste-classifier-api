import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

from core.app.waste_item.application.use_cases.list_all_items import ListAllItemsUseCase
from core.app.waste_item.application.use_cases.create_waste_item import CreateWasteItemUseCase
from core.app.waste_item.domain.entities import WasteItemType, WasteItem
from core.app.waste_item.domain.ports import WasteItemRepository

class TestListAllItems(unittest.TestCase):
    def setUp(self):
        self.waste_item_repository = Mock(spec=WasteItemRepository)

        self.use_case = ListAllItemsUseCase(
            waste_item_repository=self.waste_item_repository
        )

    def test_list_all_items(self):
        result_mock = [
            WasteItem(
                type=WasteItemType.NON_RECYCLABLE,
                material="plastic",
                approximate_weight=1.5,
                image=uuid4(),
                created_by_id=uuid4(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=uuid4(),
                id=uuid4()
            ),
            WasteItem(
                type=WasteItemType.RECYCLABLE,
                material="paper",
                approximate_weight=2.0,
                image=uuid4(),
                created_by_id=uuid4(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=uuid4(),
                id=uuid4()
            )
        ]

        self.waste_item_repository.list.return_value = result_mock

        result = self.use_case.execute()

        self.assertEqual(result, result_mock)
        self.waste_item_repository.list.assert_called_once()