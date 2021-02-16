from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import exceptions

from core import models



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = 'test@gmail.com'
        password = '123456'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized (turned to lower case) """
        email = 'test@GMAIL.COM'
        password = '123456'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    
    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='123456'
            )
    

    def test_create_new_superuser(self):
        """ Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            email='test@gmail.com',
            password='123456'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    
    def test_create_customer(self):
        """ Test creating a new customer """
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='123456'
        )
        customer = models.Customer.objects.create(
                user=user,
                customer_id=73478643,
                gender='male',
                province='Alborz',
                city='karaj',
                street='street',
                alley='alley'
            )
        
        self.assertEqual(user.email,customer.user.email)



    def test_create_customer_already_exists(self):
        """ Test creating a customer that already exists """
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='123456'
        )
        customer1 = models.Customer.objects.create(
                user=user,
                customer_id=73478643,
                gender='male',
                province='Alborz',
                city='karaj',
                street='street',
                alley='alley'
            )
        with self.assertRaises(Exception):
            customer2 = models.Customer.objects.create(
                    user=user,
                    customer_id=73478643,
                    gender='male',
                    province='Alborz',
                    city='karaj',
                    street='street',
                    alley='alley'
                )



    def test_create_personnel(self):
        """ Test creating a new personnel """
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='123456'
        )
        user.is_staff = True

        personnel = models.Personnel.objects.create(
                user=user,
                personnel_code=445455,
                gender='male',
                province='Alborz',
                city='karaj',
                street='street',
                alley='alley',
                birth_date='2015-11-23',
                age=6,
                salary=10000.25
            )
        
        self.assertEqual(user.email, personnel.user.email)

    

    def test_create_personnel_already_exists(self):
        """ Test creating a new personnel """
        user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='123456'
        )
        user.is_staff = True

        personnel1 = models.Personnel.objects.create(
                user=user,
                personnel_code=445455,
                gender='male',
                province='Alborz',
                city='karaj',
                street='street',
                alley='alley',
                birth_date='2015-11-23',
                age=6,
                salary=1000.25
            )
        with self.assertRaises(Exception):
            personnel2 = models.Personnel.objects.create(
                    user=user,
                    personnel_code=445455,
                    gender='male',
                    province='Alborz',
                    city='karaj',
                    street='street',
                    alley='alley',
                    birth_date='2015-11-23',
                    age=6,
                    salary=1000.25
                )
        