import unittest
from unittest.mock import Mock

from core.app.user.application.exceptions import UserAlreadyExists, UnableToCreateUser
from core.app.user.application.use_cases.signup import SignupUseCase
from core.app.user.domain.dtos import UserSignupDto
from core.app.user.domain.ports import UserRepository
from core.app.user.domain.entities import User


class TestSignupUserUseCase(unittest.TestCase):
    def setUp(self):
        # Setup code goes here
        self._user_repository = Mock(spec=UserRepository)

    def test_signup_user(self):
        # Arrange
        self._user_repository.create.return_value = Mock()
        self._user_repository.get_by_email.return_value = None
        use_case = SignupUseCase(user_repository=self._user_repository)

        # Act
        _ = use_case.execute(UserSignupDto(
            first_name="John",
            last_name="Doe",
            email="johndoe@email.com",
            password="password123"
        ))

        # Assert
        self._user_repository.get_by_email.assert_called_once()
        self._user_repository.create.assert_called_once()

    def test_signup_user_invalid_email(self):
        # Arrange
        self._user_repository.create.return_value = Mock()
        self._user_repository.get_by_email.return_value = Mock(spec=User)
        use_case = SignupUseCase(user_repository=self._user_repository)

        # Act
        with self.assertRaises(UserAlreadyExists):
            use_case.execute(UserSignupDto(
                first_name="John",
                last_name="Doe",
                email="jhondoe@email.com",
                password="password123"
            ))

        # Assert
        self._user_repository.get_by_email.assert_called_once()
        self._user_repository.create.assert_not_called()

    def test_signup_user_email_invalid(self):
        # Arrange
        self._user_repository.create.return_value = Mock()
        self._user_repository.get_by_email.return_value = None
        use_case = SignupUseCase(user_repository=self._user_repository)

        # Act
        with self.assertRaises(ValueError):
            use_case.execute(UserSignupDto(
                first_name="John",
                last_name="Doe",
                email="invalid-email",
                password="password123"
            ))

        # Assert
        self._user_repository.get_by_email.assert_not_called()
        self._user_repository.create.assert_not_called()

    def test_signup_user_save_fails(self):
        # Arrange
        self._user_repository.create.return_value = None
        self._user_repository.get_by_email.return_value = None
        use_case = SignupUseCase(user_repository=self._user_repository)

        # Act
        with self.assertRaises(UnableToCreateUser):
            use_case.execute(UserSignupDto(
                first_name="John",
                last_name="Doe",
                email="jhondoe@email.com",
                password="password123"
            ))

        # Assert
        self._user_repository.get_by_email.assert_called_once()
        self._user_repository.create.assert_called_once()
