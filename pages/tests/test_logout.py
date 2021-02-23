from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class LogoutTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='12345678'
        )
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_logout_get_not_allowed(self):
        """ Test get request is not allowed for logout """
        url = '/logout/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
    

    def test_logout_successful(self):
        """ Test user will logout succussfuly """
        url = '/logout/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

