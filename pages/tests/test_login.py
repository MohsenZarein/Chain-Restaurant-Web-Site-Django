from django.test import TestCase, Client
from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class LoginTests(TestCase):

    def setUp(self):
        self.client = Client()

    
    def test_login_view_get(self):
        """ Test get request for login page is ok """
        url = '/login/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_login_success(self):
        """ Test logging user successfully """
        payload = {
            'email':'test@gmail.com',
            'password':'123456'
        }
        user = create_user(**payload)
        url = '/login/'
        response = self.client.post(url,payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)
    
    """
    def test_login_fails_incorrect_credentials(self):
        # Test logging user with incorrect credentials fails
        payload = {
            'email':'test@gmail.com',
            'password':'123456'
        }
        user = create_user(**payload)
        url = '/login/'
        invalid_payload = {
            'email':'test@gmail.com',
            'password':'14511111'
        }
        response = self.client.post(url,invalid_payload)
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(user.is_authenticated)
    """
    


        

        
