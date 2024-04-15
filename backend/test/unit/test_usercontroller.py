import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

class TestUserController:
    @pytest.fixture
    def mock(self):
        return Mock()

    def test_get_user_by_email_valid(self, mock):
        mock.find.return_value = [{'email': 'smith@gmail.com', 'name': 'Smith'}]
        user_controller = UserController(mock)
        user = user_controller.get_user_by_email('smith@gmail.com')
        assert user == {'email': 'smith@gmail.com', 'name': 'Smith'}

    def test_get_user_by_email_invalid(self, mock):
        user_controller = UserController(mock)
        with pytest.raises(ValueError) as e:
            user_controller.get_user_by_email('abcd123')
        assert str(e.value) == 'Error: invalid email address'

    def test_get_user_by_email_nonexistent(self, mock):
        mock.find.return_value = none
        user_controller = UserController(mock)
        user = user_controller.get_user_by_email('nonexistent@example.com')
        assert user is None, "The user does not exist"

    def test_get_user_by_email_multiple_users(self, mock):
        return

