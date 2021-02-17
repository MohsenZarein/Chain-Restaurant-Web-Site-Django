from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from core import models


class DashboardTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='123456'
        )
        self.client = Client()
        self.client.force_login(user=self.user)
    

    def test_dashboard_view_get(self):
        """ Test get request to customer dashboard """
        url = '/customer/dashboard'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)