from django.db import models
from core.models import Base, StatusMixin, BaseDiscount
from account.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.

class Category(Base):
    category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='categorys', blank=True, null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/')
    column = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.name}-{self.column}'


class Discount(BaseDiscount):
    CUSTOM_NUMBER = 'number'
    CUSTOM_PERECENT = 'perecent'
    CUSTOM_DISCOUNT = (
        (CUSTOM_NUMBER, 'NUMBER'),
        (CUSTOM_PERECENT, 'PERECENT'),
    )
    type = models.CharField(choices=CUSTOM_DISCOUNT, max_length=8)
    amount = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField(blank=True, null=True)
    discount_code = models.CharField(max_length=20, blank=True, null=True)

    def clean(self):
        if self.start < timezone.now():
            raise ValidationError({'start': ' تاریخ شروع نباید برای گذشته باشد '})

        if self.expire < self.start + timedelta(days=1):
            raise ValidationError({'expire': ' تاریخ انقضا باید یک روز بیشتر از شروع باشد '})
        if self.type == self.CUSTOM_PERECENT and isinstance(self.amount, int) and self.amount > 100:
            raise ValidationError({'dis': ' این فیلد نباید بیشتر از صد درصد باشد  '})

        if self.type == self.CUSTOM_NUMBER and self.max_amount:
            raise ValidationError({'max_dis': 'این فیلد باید خالی باشد '})

        if self.type == self.CUSTOM_PERECENT and self.discount_code:
            raise ValidationError({'discount_code': 'این فیلد باید خالی باشد '})

        if isinstance(self.max_amount, int) and self.max_amount > 100:
            raise ValidationError({'max_dis': '  این فیلد نباید بیشتر از صد درصد باشد  '})

    def __str__(self) -> str:
        return f'{self.amount}-{self.type}'


class Product(Base, StatusMixin):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    Specifications = models.TextField(max_length=200)
    inventory = models.IntegerField()
    price = models.PositiveIntegerField()
    price_discount = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='discount_product', null=True,
                                 blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    image = models.ImageField(upload_to='product/')
    color = models.CharField(max_length=20, default='black')

    def clean(self):

        if self.discount:
            if self.discount.type == 'number' and self.price < self.discount.amount:
                raise ValidationError({'discount': '  تخفیف نباید بیشتر از قیمت باشد '})
        #     if self.discount.type =='perecent':
        #         self.price_discount= (self.price*self.discount.amount)/100
        #     if self.discount.type =='number':
        #         self.price_discount= self.price-self.discount.amount
        # else :
        #     self.price_discount= self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            counter = 1
            self.slug = slugify(f'{self.name}') + f'-{counter}'
            while Product.objects.filter(slug=self.slug).exists():
                counter += 1
                self.slug = slugify(f'{self.name}') + f'-{counter}'
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'name:{self.name}-price:{self.price_discount}-inventory:{self.inventory}'

    def count_likes(self):
        count = self.product_like.count()
        return count

    def count_comment(self):
        count = self.product_comment.count()
        return count



    def can_like(self, user):
        # can=Like.objects.filter(user=user,product=product).exists()
        can = user.like.filter(product=self).first()
        print('masoud', can)
        if can and can.is_deleted == False:
            return False
        return True

    def exist_like(self, user):
        # can=Like.objects.filter(user=user,product=product).exists()
        can = user.like.filter(product=self).exists()
        if can:
            return True
        return False

    # def counter_cell_product(self):
    #     # orderitems=OrderItem.objects.filter(product=self)
    #     # sum_cell=sum([item.count for item in orderitems])
    #     return 'sum_cell'


class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Like(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_like')

    def clean(self):
        can = Like.objects.filter(user=self.user, product=self.product).exists()
        if can:
            raise ValidationError({'user': '  یک بار بیشتر نمیتوانید این محصول  را  لایک کنید  '})

    def __str__(self) -> str:
        return f'liked by {self.user}'


class Comment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comment')
    comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)

    def __str__(self) -> str:
        return f'{self.user}-{self.body}'
