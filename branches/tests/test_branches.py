from django.test import TestCase, Client
from core.models import Branch

class BranchTests(TestCase):

    def setUp(self):

        self.client = Client()

    
    def test_view_branch_detail(self):
        """ Test viewing a branch detail """
        branch = Branch.objects.create(
            province='Tehran',
            city='Tehran',
            street='street',
            alley='alley',
            phone='02177777',
            branch_code=48545145
        )

        url = '/branch/{0}'.format(branch.branch_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['branch'].branch_code, branch.branch_code)