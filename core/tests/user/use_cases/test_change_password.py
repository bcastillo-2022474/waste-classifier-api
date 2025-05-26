import unittest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from core.app.user.application.use_cases.change_password import ChangePasswordUseCase
from core.app.user.application.exceptions import UserNotFoundException, UnauthorizedUserException
from core.app.user.application.use_cases.dto import ChangePasswordDTO
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User


class TestChangePasswordUseCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = ChangePasswordUseCase(user_repository=self.user_repository)
        self.user_id = uuid4()
        now = datetime.now()
        self.user = User(
            id=self.user_id,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            is_active=True,
            date_joined=now,
            created_at=now,
            updated_at=now,
            created_by_id=None
        )

    def test_change_password_success(self):
        # Arrange
        self.user_repository.get_by_id.return_value = self.user
        self.user_repository.check_password.return_value = True
        self.user_repository.update_password.return_value = None

        payload = ChangePasswordDTO(
            current_password="old_password123",
            new_password="new_password456"
        )

        # Act
        self.use_case.execute(self.user_id, payload)

        # Assert
        self.user_repository.get_by_id.assert_called_once_with(self.user_id)
        self.user_repository.check_password.assert_called_once_with(
            user_id=self.user_id,
            current_password="old_password123"
        )
        self.user_repository.update_password.assert_called_once_with(
            user_id=self.user_id,
            new_password="new_password456"
        )

    def test_change_password_user_not_found(self):
        # Arrange
        self.user_repository.get_by_id.return_value = None
        payload = ChangePasswordDTO(
            current_password="old_password123",
            new_password="new_password456"
        )

        # Act & Assert
        with self.assertRaises(UserNotFoundException) as context:
            self.use_case.execute(self.user_id, payload)

        # Assert
        self.assertIn(str(self.user_id), str(context.exception))
        self.user_repository.get_by_id.assert_called_once_with(self.user_id)
        self.user_repository.check_password.assert_not_called()
        self.user_repository.update_password.assert_not_called()

    def test_change_password_incorrect_current_password(self):
        # Arrange
        self.user_repository.get_by_id.return_value = self.user
        self.user_repository.check_password.return_value = False

        payload = ChangePasswordDTO(
            current_password="wrong_password",
            new_password="new_password456"
        )

        # Act & Assert
        with self.assertRaises(UnauthorizedUserException) as context:
            self.use_case.execute(self.user_id, payload)

        # Assert
        self.assertEqual(str(context.exception), "Passwords do not match")
        self.user_repository.get_by_id.assert_called_once_with(self.user_id)
        self.user_repository.check_password.assert_called_once_with(
            user_id=self.user_id,
            current_password="wrong_password"
        )
        self.user_repository.update_password.assert_not_called()

    def test_change_password_invalid_dto_short_current_password(self):
        # Arrange & Act & Assert
        with self.assertRaises(ValidationError):
            ChangePasswordDTO(
                current_password="",  # Empty password
                new_password="new_password456"
            )

        # Assert repository methods are not called since DTO creation failed
        self.user_repository.get_by_id.assert_not_called()
        self.user_repository.check_password.assert_not_called()
        self.user_repository.update_password.assert_not_called()

    def test_change_password_invalid_dto_short_new_password(self):
        # Arrange & Act & Assert
        with self.assertRaises(ValidationError):
            ChangePasswordDTO(
                current_password="current_password123",
                new_password="short"  # Too short (less than 8 characters)
            )

        # Assert repository methods are not called since DTO creation failed
        self.user_repository.get_by_id.assert_not_called()
        self.user_repository.check_password.assert_not_called()
        self.user_repository.update_password.assert_not_called()

    def test_change_password_invalid_dto_missing_fields(self):
        # Arrange & Act & Assert
        with self.assertRaises(ValidationError):
            ChangePasswordDTO()  # Missing required fields

        # Assert repository methods are not called since DTO creation failed
        self.user_repository.get_by_id.assert_not_called()
        self.user_repository.check_password.assert_not_called()
        self.user_repository.update_password.assert_not_called()
