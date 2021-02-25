from django.test import TestCase, Client
from django.contrib.auth import get_user_model



class PessonelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='perssonel@gmail.com',
            password='password'
        )
        self.user.is_staff = True

        self.client = Client()
        self.client.force_login(user=self.user)

    
    def test_viewing_dashborad(self):
        """ Test perssonel view their dashboard correctly """
        url = 'perssonel/perssonel-dashboard'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
