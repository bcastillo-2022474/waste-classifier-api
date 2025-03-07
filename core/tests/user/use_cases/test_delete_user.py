import unittest
from unittest.mock import Mock
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User
from core.app.user.application.exceptions import UserNotFoundException
from uuid import uuid4
from datetime import datetime
from core.app.user.application.use_cases.get_self_user import GetSelfUserUseCase

class TestGetSelfUserUseCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = GetSelfUserUseCase(
            user_repository=self.user_repository
        )
    
    def test_get_self_user(self):
        user_id = uuid4()
        user_mock = User(
        id=user_id,
        first_name="John",
        last_name="Doe",
        email="carlosaltan@gmail.com",
        is_active=True,
        date_joined=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by_id=uuid4()
        )

        self.user_repository.get.return_value = user_mock
        result = self.use_case.execute(user_id=user_id)
        self.assertEqual(result, user_mock)
        self.user_repository.get.assert_called_once() 

    def test_get_self_user_not_found(self):
        user_id = uuid4()
        self.user_repository.get.return_value = None
        with self.assertRaises(UserNotFoundException):
            self.use_case.execute(user_id=user_id)
        self.user_repository.get.assert_called_once()
