from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from core.models import Branch, OnlineOrder, Customer, Food


class OrderFoodTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='123456'
        )
        self.client = Client()
        self.client.force_login(user=self.user)


    def test_order_view_get(self):
        """ Test get request to order page is ok """
        branch = Branch.objects.create(
            branch_code='1234'
        )
        url = f'/order/{branch.branch_code}'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code , 200)


    def test_order_food(self):
        """ Test an ordered food is added to shop basket """
        branch = Branch.objects.create(
            branch_code=1234
        )
        customer =  Customer.objects.create(
            user=self.user,
            customer_id=1111
        )
        food = Food.objects.create(
            name='کباب کوبیده',
            price=10000,
            description='کباب کوبیده به همراه مخلفات'
        )

        url = f'/order/{branch.branch_code}'

        payload = {
            'food_id':food.pk,
            'count':2,
        }

        response = self.client.post(url,payload)

        self.assertEqual(response.status_code, 200)

        order = OnlineOrder.objects.get(
            customer=customer,
            branch=branch,
            food=food
        )

        self.assertEqual(order.customer.customer_id, customer.customer_id)
        self.assertEqual(order.branch.branch_code, branch.branch_code)
        self.assertEqual(order.food.pk, food.pk)
        self.assertEqual(order.count, payload['count'])



