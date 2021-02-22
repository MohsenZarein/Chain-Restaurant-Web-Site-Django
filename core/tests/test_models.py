from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import exceptions

from core import models
from uuid import uuid4



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

    def test_branch_str(self):
        """ Test the branch string representation
            (creating a branch succussfuly)
        """
        branch = models.Branch.objects.create(
            province='province',
            city='city',
            street='street',
            alley='alley',
            phone='+989127777777',
            branch_code=12345678
        )

        self.assertEqual(str(branch), branch.province + '-' + branch.city)
    

    def test_food_str(self):
        """ Test the food string representaion 
            (creating a food succussfuly)
        """
        food = models.Food.objects.create(
            name='کباب کوبیده',
            price=30000,
            description='کباب کوبیده  به همراه مخلفات',
            category='breakfasts'
        )

        self.assertEqual(food.category, 'breakfasts')
        self.assertEqual(str(food), food.name)


    def test_table_str(self):
        """ Test the table string representaion
            (creating a table succussfuly)
        """
        branch = models.Branch.objects.create(
            branch_code=1111,
        )
        table = models.Table.objects.create(
            is_empty=True,
            is_reserved=False,
            capacity=4,
            branch=branch
        )

        self.assertEqual(str(table), str(table.pk))

    
    def test_order_online_str(self):
        """ Test the online order string representaion
            (adding an online order succussfuly)
        """
        branch = models.Branch.objects.create(
            branch_code=1234
        )
        customer =  models.Customer.objects.create(
            user=get_user_model().objects.create_user(
                email='test1@gmail.com',
                password=4141
            ),
            customer_id=1111
        )
        food = models.Food.objects.create(
            name='کباب کوبیده',
            price=10000,
            description='کباب کوبیده به همراه مخلفات'
        )
        user = get_user_model().objects.create_user(
                email='test2@gmai.com',
                password='123',
            )
        user.is_staff = True
        deliverer = models.Personnel.objects.create(
            user=user,
            personnel_code=4545,
            gender='male',
            province='Alborz',
            city='karaj',
            street='street',
            alley='alley',
            birth_date='2015-11-23',
            age=6,
            salary=10000.25
        )

        order = models.OnlineOrder.objects.create(
            customer=customer,
            branch=branch,
            food=food,
            deliverer=deliverer,
            pay_code=str(uuid4()),
            count=2
        )

        self.assertEqual(str(order), order.pay_code)