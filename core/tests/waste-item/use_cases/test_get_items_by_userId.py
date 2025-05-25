import unittest
from unittest.mock import MagicMock
from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.exceptions import WasteItemNotFoundException
from core.app.waste_item.application.use_cases.get_items_by_userId import GetItemsByUserIdUseCase

class DummyWasteItem:
    pass

class TestGetItemsByUserIdUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=WasteItemRepository)
        self.use_case = GetItemsByUserIdUseCase(self.mock_repository)

    def test_execute_returns_items_for_existing_user(self):
        user_id = "user-123"
        expected_items = [DummyWasteItem(), DummyWasteItem()]
        self.mock_repository.list_by_user_id.return_value = expected_items

        result = self.use_case.execute(user_id)

        self.mock_repository.list_by_user_id.assert_called_once_with(user_id)
        self.assertEqual(result, expected_items)

    def test_execute_raises_exception_when_no_items_found(self):
        user_id = "user-456"
        self.mock_repository.list_by_user_id.return_value = []

        with self.assertRaises(WasteItemNotFoundException):
            self.use_case.execute(user_id)
        self.mock_repository.list_by_user_id.assert_called_once_with(user_id)

if __name__ == "__main__":
    unittest.main()