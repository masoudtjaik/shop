from django.test import TestCase
from order.models import Order, OrderItem
from model_bakery import baker
from account.models import User
from products.models import Product
from django.core.exceptions import ValidationError

class TestOrder(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')
        self.order = baker.make(Order, user=self.user, total=1000)

    def test_model_save(self):
        self.assertEqual(self.order.slug, 'masoudtj-masoud123gmailcom-1000')

    def test_model_str(self):
        self.assertEqual(str(self.order), 'masoudtj-masoud123gmailcom-1000')


class TestOrderItem(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')
        self.product = baker.make(Product, name='product', price_discount=1000, inventory=10, )
        self.product2 = baker.make(Product, name='product2', price_discount=1000, inventory=10, )
        self.order_item = baker.make(OrderItem, user=self.user, product=self.product, count=2)
        self.order_item_clean = baker.make(OrderItem, user=self.user, product=self.product, count=12)
        #test orderitem cell
        self.order=baker.make(Order,user=self.user)
        self.orderitem=baker.make(OrderItem,user=self.user,product=self.product,order=self.order,count=2)
        self.orderitem2=baker.make(OrderItem,user=self.user,product=self.product,order=self.order,count=3)
        self.orderitem3=baker.make(OrderItem,user=self.user,product=self.product2,order=self.order,count=3)
        self.orderitem4=baker.make(OrderItem,user=self.user,product=self.product2,order=self.order,count=3)

    # def test_model_get_count(self):
    #     self.assertEqual(self.order_item.get_count(), 2000)

    def test_model_clean(self):
        with self.assertRaises(ValidationError):
            self.order_item_clean.clean()

    def test_model_save(self):
        self.assertEqual(self.order_item.slug, 'masoudtj-masoud123gmailcom-2')

    def test_model_str(self):
        self.assertEqual(str(self.order_item), 'masoudtj-masoud123gmailcom-2')
        
    def test_counter_cell_product(self):
        print(OrderItem.counter_cell_product(self.product2))
        self.assertEqual(OrderItem.counter_cell_product(self.product), 19)
        
    def test_top_cell_productt(self):
        print(OrderItem.top_cell_product())
        # self.assertEqual(self.orderitem.counter_cell_product(), 19)   