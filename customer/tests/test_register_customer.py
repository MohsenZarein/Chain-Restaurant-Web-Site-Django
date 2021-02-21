from django.test import TestCase, Client
from core.models import Customer
from django.contrib.auth import get_user_model
from django.core import exceptions



class RegisterTests(TestCase):

    def setUp(self):

        self.client = Client()


    def test_register_view_get(self):
        """ Test get request for register page is ok """
        url = '/customer/register'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        

    def test_register_succesful(self):
        """ Test registering customer with valid payload is successful """
        payload = {
            'email':'test@gmail.com',
            'first_name':'Ali',
            'last_name':'Akbari',
            'password1':'123456',
            'password2':'123456',
            'phone':'09121111'
        }

        url = '/customer/register'
        response = self.client.post(url,payload)

        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.get(email=payload['email'])
        customer = Customer.objects.get(user=user)
        self.assertEqual(customer.user.email, user.email)
        self.assertTrue(user.check_password(payload['password1']))

        
    def test_register_customer_already_exists(self):
        """ Test registering a customer that already exists fails """
        payload = {
            'email':'test@gmail.com',
            'first_name':'Ali',
            'last_name':'Akbari',
            'password1':'123456',
            'password2':'123456',
            'phone':'091211111'
        }

        get_user_model().objects.create_user(
            email=payload['email'],
            password=payload['password1']
        )

        url = '/customer/register'
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 302)
     
        try:
            get_user_model().objects.get(email=payload['email'])
            status = True
        except exceptions.MultipleObjectsReturned:
            status = False
        
        self.assertTrue(status)
            





