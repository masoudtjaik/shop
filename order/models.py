from django.db import models
from core.models import Base, BaseOrder
from account.models import User
from products.models import Discount, Product
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# Create your models here.

class Order(BaseOrder):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    total = models.PositiveIntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='discount_order', null=True,
                                 blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user}-{self.total}')
        super().save(*args, **kwargs)

    # def get_total(self):
    #     # return sum(item.get_count() for item in self.order_orderitem.all() )
    #     return self.order_orderitem.get_count()

    def __str__(self) -> str:
        return f'{self.slug}'


class OrderItem(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orderitem', )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_orderitem')
    slug = models.SlugField(null=True, blank=True)
    count = models.PositiveIntegerField()

    def clean(self):
        if self.count == 0:
            raise ValidationError({'count': ' تعداد باید حداقل 1 باشد '})
        if self.product:
            if self.count and self.product.inventory < self.count:
                raise ValidationError({'count': ' این تعداد موجودی ندارد '})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user}-{self.product}')
            # self.product.inventory -=self.count
            # self.product.save()
            # product=Product.objects.get(pk=self.product.id)
            # product.inventory -= self.count
            # product.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.slug}'

    def get_count(self):
        return self.product.price_discount * self.count
