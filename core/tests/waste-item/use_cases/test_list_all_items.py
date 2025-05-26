import unittest
from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4, UUID
from dataclasses import dataclass
from enum import Enum

# Simulación de WasteItemType y WasteItem (ajústalo si ya está implementado correctamente en tu proyecto)
class WasteItemType(Enum):
    RECYCLABLE = "recyclable"
    NON_RECYCLABLE = "non_recyclable"

@dataclass
class WasteItem:
    type: WasteItemType
    material: str
    approximate_weight: float
    image: UUID
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    id: UUID

# Simulación de WasteItemRepository y ListAllItemsUseCase
class WasteItemRepository:
    def list(self):
        pass

class ListAllItemsUseCase:
    def __init__(self, waste_item_repository: WasteItemRepository):
        self.waste_item_repository = waste_item_repository

    def execute(self):
        return self.waste_item_repository.list()

# Test
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
