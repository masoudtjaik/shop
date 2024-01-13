from django.db import models
from core.models import Base
from account.models import User
from products.models import Discount, Product
from django.utils.text import slugify


# Create your models here.

class Order(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    total = models.PositiveIntegerField()
    slug = models.SlugField(null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='discount_order', null=True,
                                 blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user}-{self.total}')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.slug}'


class OrderItem(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orderitem',)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_orderitem')
    slug = models.SlugField(null=True, blank=True)
    count = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user}-{self.product}')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.slug}'
