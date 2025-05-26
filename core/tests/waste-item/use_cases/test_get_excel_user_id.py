import unittest
from unittest.mock import Mock
from core.app.waste_item.application.use_cases.get_excel_user_id import GetExcelByUserIdUseCase


class TestGetExcelByUserIdUseCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test dependencies before each test."""
        self.mock_repository = Mock()
        self.use_case = GetExcelByUserIdUseCase(self.mock_repository)

    def test_execute_calls_repository_with_user_id(self):
        """Test that execute calls repository with correct user_id."""
        # Arrange
        user_id = "user-123"
        mock_response = Mock()  # Mock HttpResponse
        mock_response.content = b"fake excel content"
        mock_response.__getitem__ = Mock(return_value="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(result, mock_response)

    def test_execute_with_empty_user_id_calls_repository(self):
        """Test that execute handles empty user ID by passing it to repository."""
        # Arrange
        user_id = ""
        mock_response = Mock()
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(result, mock_response)

    def test_execute_with_none_user_id_calls_repository(self):
        """Test that execute handles None user ID by passing it to repository."""
        # Arrange
        user_id = None
        mock_response = Mock()
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(result, mock_response)

    def test_execute_propagates_repository_exception(self):
        """Test that execute properly propagates exceptions from repository."""
        # Arrange
        user_id = "user-456"
        error_message = "Database connection failed"
        self.mock_repository.get_excel.side_effect = Exception(error_message)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.use_case.execute(user_id)

        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(str(context.exception), error_message)

    def test_execute_propagates_specific_exceptions(self):
        """Test that execute propagates specific exception types from repository."""
        # Arrange
        user_id = "user-789"
        self.mock_repository.get_excel.side_effect = ValueError("Invalid user ID format")

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.use_case.execute(user_id)

        self.mock_repository.get_excel.assert_called_once_with(user_id)
        self.assertEqual(str(context.exception), "Invalid user ID format")

    def test_execute_with_different_user_ids_calls_repository_correctly(self):
        """Test that execute correctly passes different user IDs to repository."""
        # Test with multiple user IDs
        test_cases = [
            "user-001",
            "admin-user", 
            "12345",
            "user@example.com"
        ]

        for user_id in test_cases:
            with self.subTest(user_id=user_id):
                # Arrange
                mock_response = Mock()
                self.mock_repository.get_excel.return_value = mock_response
                self.mock_repository.reset_mock()

                # Act
                result = self.use_case.execute(user_id)

                # Assert
                self.mock_repository.get_excel.assert_called_once_with(user_id)
                self.assertEqual(result, mock_response)

    def test_execute_returns_exact_repository_response(self):
        """Test that execute returns exactly what repository returns."""
        # Arrange
        user_id = "user-test"
        mock_response = Mock()
        mock_response.content = b"Excel data with headers and rows"
        mock_response.__getitem__ = Mock(side_effect=lambda key: {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': 'attachment; filename="test.xlsx"'
        }.get(key, ''))
        
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.assertEqual(result, mock_response)
        self.assertEqual(result['Content-Disposition'], 'attachment; filename="test.xlsx"')

    def test_constructor_stores_repository_correctly(self):
        """Test that constructor properly stores the repository dependency."""
        # Arrange & Act
        use_case = GetExcelByUserIdUseCase(self.mock_repository)

        # Assert
        self.assertEqual(use_case.repository, self.mock_repository)

    def test_multiple_executions_call_repository_multiple_times(self):
        """Test that multiple executions result in multiple repository calls."""
        # Arrange
        user_id = "user-multi"
        mock_response = Mock()
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        self.use_case.execute(user_id)
        self.use_case.execute(user_id)
        self.use_case.execute(user_id)

        # Assert
        self.assertEqual(self.mock_repository.get_excel.call_count, 3)
        self.mock_repository.get_excel.assert_called_with(user_id)

    def test_repository_method_called_with_correct_parameters(self):
        """Test that repository method is called with exact parameters."""
        # Arrange
        user_id = "specific-user-123"
        mock_response = Mock()
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        self.use_case.execute(user_id)

        # Assert
        # Verify the exact call arguments
        call_args = self.mock_repository.get_excel.call_args
        self.assertEqual(call_args[0][0], user_id)  # First positional argument
        self.assertEqual(len(call_args[0]), 1)      # Only one argument passed

    def test_use_case_does_not_modify_repository_response(self):
        """Test that use case returns repository response without modification."""
        # Arrange
        user_id = "test-user"
        mock_response = Mock()
        original_content = b"original excel content"
        mock_response.content = original_content
        mock_response.custom_attr = "custom_value"
        self.mock_repository.get_excel.return_value = mock_response

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.assertIs(result, mock_response)  # Exact same object reference
        self.assertEqual(result.content, original_content)
        self.assertEqual(result.custom_attr, "custom_value")

    def test_execute_with_various_exception_types(self):
        """Test that execute handles various exception types from repository."""
        exception_test_cases = [
            (ConnectionError("Network error"), ConnectionError),
            (FileNotFoundError("File not found"), FileNotFoundError),
            (PermissionError("Access denied"), PermissionError),
            (RuntimeError("Runtime issue"), RuntimeError)
        ]

        for exception, expected_type in exception_test_cases:
            with self.subTest(exception=exception):
                # Arrange
                user_id = "test-user"
                self.mock_repository.get_excel.side_effect = exception
                self.mock_repository.reset_mock()

                # Act & Assert
                with self.assertRaises(expected_type):
                    self.use_case.execute(user_id)
                
                self.mock_repository.get_excel.assert_called_once_with(user_id)


if __name__ == "__main__":
    unittest.main()