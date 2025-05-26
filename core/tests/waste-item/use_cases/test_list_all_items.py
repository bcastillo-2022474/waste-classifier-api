import unittest
from unittest.mock import Mock
from core.app.waste_item.application.use_cases.list_all_items import ListAllItemsUseCase

class TestListAllItemsUseCase(unittest.TestCase):

    def setUp(self):
        self.mock_repository = Mock()
        self.use_case = ListAllItemsUseCase(self.mock_repository)

    def test_execute_returns_all_items_from_repository(self):
        mock_items = [Mock(), Mock()]
        self.mock_repository.list_item.return_value = mock_items

        result = self.use_case.execute()

        self.mock_repository.list_item.assert_called_once()
        self.assertEqual(result, mock_items)

    def test_execute_returns_empty_list_when_no_items(self):
        self.mock_repository.list_item.return_value = []

        result = self.use_case.execute()

        self.mock_repository.list_item.assert_called_once()
        self.assertEqual(result, [])

    def test_execute_propagates_repository_exceptions(self):
        self.mock_repository.list_item.side_effect = Exception("Database connection failed")

        with self.assertRaises(Exception) as context:
            self.use_case.execute()

        self.mock_repository.list_item.assert_called_once()
        self.assertEqual(str(context.exception), "Database connection failed")

if __name__ == "__main__":
    unittest.main()
