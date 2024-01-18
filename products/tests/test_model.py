from django.test import TestCase
from order.models import Order, OrderItem
from model_bakery import baker
from account.models import User
from products.models import Product,Category,Discount,Comment,Like
from django.core.exceptions import ValidationError
from order.models import OrderItem
class TestCategory(TestCase):
    def setUp(self) -> None:
        self.category = baker.make(Category, name='category1',column=2)

    def test_model_str(self):
        self.assertEqual(str(self.category), 'category1-2')


class TestProduct(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')
        self.user2 = baker.make(User, username='meysamtj', email='meysam123@gmail.com')
        self.product = baker.make(Product, name='product', price_discount=1000, inventory=10,price=1000)
        self.like = baker.make(Like, user=self.user,product=self.product)
        self.like2 = baker.make(Like, user=self.user,product=self.product)
        self.like3 = baker.make(Like, user=self.user,product=self.product)
        self.comment = baker.make(Comment, user=self.user,body='testnew',product=self.product)
        self.comment2 = baker.make(Comment, user=self.user,body='testnew',product=self.product)
        self.discount = baker.make(Discount, type='number', amount=2000)
        self.product_clean = baker.make(Product, name='product',price=1000 ,inventory=10,discount=self.discount )
        
        
        

    
    # def clean(self):
        
    #     if self.discount:
    #         if self.discount.type == 'number' and self.price < self.discount.amount:
    #             raise ValidationError({'discount': '  تخفیف نباید بیشتر از قیمت باشد '})

    def test_model_clean(self):
            with self.assertRaises(ValidationError):
                self.product_clean.clean()
                
    def test_count_can_like(self):
        self.assertFalse(self.product.can_like(self.user))
        self.assertTrue(self.product.can_like(self.user2))
    
    def test_count_like(self):
        self.assertEqual(self.product.count_likes(),3)
    
    def test_count_like(self):
        self.assertEqual(self.product.count_comment(),2)

    def test_model_save(self):
        self.assertEqual(self.product.slug, 'product-10')

    
        


class TestDiscount(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')
        self.order = baker.make(Order, user=self.user, total=1000)
        self.discount = baker.make(Discount, type='number', amount=2000)


    def test_model_str(self):
        self.assertEqual(str(self.discount), '2000-number')
        
        
class TestComment(TestCase):
    def setUp(self) -> None:
        
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')
        self.comment = baker.make(Comment, user=self.user,body='testnew')


    def test_model_str(self):
        self.assertEqual(str(self.comment), 'masoudtj-masoud123@gmail.com-testnew')
        
        
class TestLike(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, username='masoudtj', email='masoud123@gmail.com')
        
        self.product = baker.make(Product, name='product', price_discount=1000, inventory=10 )
        self.like = baker.make(Like, user=self.user,product=self.product)
        self.like2 = baker.make(Like, user=self.user,product=self.product)
        self.like3 = baker.make(Like, user=self.user,product=self.product)
    def test_model_clean(self):
        with self.assertRaises(ValidationError):
            self.like3.clean()

    def test_model_str(self):
        self.assertEqual(str(self.like), 'liked by masoudtj-masoud123@gmail.com')