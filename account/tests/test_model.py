from django.test import TestCase
from account.models import User, Address
from model_bakery import baker


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')

    def test_model_str(self):
        self.assertEqual(str(self.user), 'masoudtj-masoud123@gmail.com')


class TestAddress(TestCase):
    def setUp(self) -> None:
        self.address = baker.make(Address, city='tehran', street='gharb')

    def test_model_str(self):
        self.assertEqual(str(self.address), 'tehran-gharb')
