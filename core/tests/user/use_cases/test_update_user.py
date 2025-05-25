import unittest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime

from core.app.user.application.use_cases.update_user import UpdateUserUseCase
from core.app.user.application.exceptions import UserNotFoundException
from core.app.user.application.use_cases.dto import UpdateUserDTO
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User

class TestUpdateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = UpdateUserUseCase(user_repository=self.user_repository)
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

    def test_update_user_success(self):
        self.user_repository.get.return_value = self.user
        self.user_repository.update.return_value = self.user

        user_data = UpdateUserDTO(first_name="Jane", last_name="Smith", email="jane@example.com")
        updated_user = self.use_case.execute(self.user_id, user_data)

        self.user_repository.get.assert_called_once_with(self.user_id)
        self.user_repository.update.assert_called_once()
        self.assertEqual(updated_user, self.user)

    def test_update_user_not_found(self):
        self.user_repository.get.return_value = None
        user_data = UpdateUserDTO(first_name="Jane")

        with self.assertRaises(UserNotFoundException):
            self.use_case.execute(self.user_id, user_data)

    def test_update_user_invalid_data(self):
        self.user_repository.get.return_value = self.user
        # Esto lanzará un error de validación de pydantic
        with self.assertRaises(ValueError):
            UpdateUserDTO(email="not-an-email")