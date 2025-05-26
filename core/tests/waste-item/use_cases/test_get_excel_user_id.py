import unittest
from unittest.mock import Mock
from core.app.waste_item.application.use_cases.get_excel_user_id import GetExcelByUserIdUseCase


class TestGetExcelByUserIdUseCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test dependencies before each test."""
        self.mock_repository = Mock()
        self.use_case = GetExcelByUserIdUseCase(self.mock_repository)

    def test_execute_successfully_returns_excel_data(self):
        """Test that execute returns Excel data when repository call succeeds."""
        # Arrange
        user_id = "user-123"
        expected_excel_data = Mock()
        expected_excel_data.content = b"excel_file_content"
        expected_excel_data.headers = {"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
        self.mock_repository.get_excel.return_value = expected_excel_data

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(result, expected_excel_data)

    def test_execute_handles_edge_cases_for_user_id(self):
        """Test that execute properly handles edge cases by delegating to repository."""
        edge_cases = [None, "", "  "]
        
        for user_id in edge_cases:
            with self.subTest(user_id=user_id):
                # Arrange
                self.mock_repository.reset_mock()
                mock_response = Mock()
                self.mock_repository.get_excel.return_value = mock_response

                # Act
                result = self.use_case.execute(user_id)

                # Assert
                self.mock_repository.get_excel.assert_called_once_with(user_id)
                self.assertEqual(result, mock_response)

    def test_execute_propagates_repository_exceptions(self):
        """Test that execute properly propagates exceptions from repository layer."""
        # Arrange
        user_id = "user-456"
        repository_error = ValueError("Invalid user ID format")
        self.mock_repository.get_excel.side_effect = repository_error

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.use_case.execute(user_id)

        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(str(context.exception), "Invalid user ID format")


if __name__ == "__main__":
    unittest.main()