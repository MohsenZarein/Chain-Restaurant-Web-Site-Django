from django.test import TestCase, Client


class IndexTests(TestCase):

    def setUp(self):

        self.client = Client()
    

    def test_index(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
