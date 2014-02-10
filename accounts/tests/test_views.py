from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from unittest.mock import patch

User = get_user_model() #1

from accounts.views import login


class LoginViewTest(TestCase):
	
    @patch('accounts.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(
        self, mock_authenticate
    ):
        mock_authenticate.return_value = None #3
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_once_with(assertion='assert this') #4


    @patch('accounts.views.authenticate')
    def test_returns_OK_when_user_found(
        self, mock_authenticate
    ):
        user = User.objects.create(email='a@b.com')
        user.backend = '' # required for auth_login to work
        mock_authenticate.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(response.content.decode(), 'OK')


    @patch('accounts.views.auth_login')
    @patch('accounts.views.authenticate')
    def test_calls_auth_login_if_authenticate_returns_a_user(
        self, mock_authenticate, mock_auth_login
    ):
        request = HttpRequest()
        request.POST['assertion'] = 'asserted'
        mock_user = mock_authenticate.return_value
        login(request)
        mock_auth_login.assert_called_once_with(request, mock_user)


    @patch('accounts.views.auth_login')
    @patch('accounts.views.authenticate')
    def test_does_not_call_auth_login_if_authenticate_returns_None(
        self, mock_authenticate, mock_auth_login
    ):
        request = HttpRequest()
        request.POST['assertion'] = 'asserted'
        mock_authenticate.return_value = None
        login(request)
        self.assertFalse(mock_auth_login.called)