from django.db import models
from core.models import Base
from account.models import User
from django.utils.text import slugify    
from django.core.exceptions import ValidationError 
# Create your models here.

class Category(Base):
    category=models.ForeignKey('self',on_delete=models.CASCADE,related_name='categorys',blank=True,null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='covers/', blank=True,null=True)
    column=models.IntegerField()
    
    def __str__(self) -> str:
        return f'{self.name}'

class Discount(models.Model):
    CUSTOM_NUMBER = 'number'
    CUSTOM_PERECENT = 'perecent'
    CUSTOM_DISCOUNT = (
        (CUSTOM_NUMBER,'NUMBER'),
        (CUSTOM_PERECENT,'PERECENT'),
    )
    type = models.CharField(choices=CUSTOM_DISCOUNT,max_length=8)
    dis=models.PositiveIntegerField()
    max_dis=models.PositiveIntegerField(blank=True,null=True)
    discount_code=models.IntegerField(blank=True,null=True)
    
    def clean(self) :
        if self.type==self.CUSTOM_PERECENT and isinstance(self.dis,int) and  self.dis>100:
            raise ValidationError({'dis':' این فیلد نباید بیشتر از صد درصد باشد  '})
        
        if self.type==self.CUSTOM_NUMBER and self.max_dis:
            raise ValidationError({'max_dis':'این فیلد باید خالی باشد '})
        
        if isinstance(self.max_dis,int) and  self.max_dis>100:
            raise ValidationError({'max_dis':'  این فیلد نباید بیشتر از صد درصد باشد  '})
        
        
    def __str__(self) -> str:
        return f'{self.dis}'
    

class Product(Base):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    Specifications = models.CharField(max_length=50)
    mojodi = models.IntegerField()
    price = models.PositiveIntegerField()
    slug=models.SlugField(blank=True,null=True)
    discount=models.ForeignKey(Discount,on_delete=models.CASCADE,related_name='discount_product',null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_product')
    image = models.ImageField(upload_to='covers/', blank=True,null=True)
    def clean(self) :
        if self.discount:
             if   self.discount.type=='number' and self.price<self.discount.dis:
                raise ValidationError({'discount':'  تخفیف نباید بیشتر از قیمت باشد '})
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(f'{self.name}')
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.name}-{self.price}'
    
    def count_likes(self):
        count=self.product_like.count()
        return count
    
    def count_comment(self):
        count=self.product_comment.count()
        return count
    
    def can_like(self,user):
        # can=Like.objects.filter(user=user,product=product).exists()
        can=user.like.filter(product=self).exists()
        if can:
            return False
        return True
    
class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='like')
    product=models.ForeignKey(User,on_delete=models.CASCADE,related_name='product_like')
    
    def __str__(self) -> str:
        return f'liked by {self.user}'

class Comment(Base):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    product=models.ForeignKey(User,on_delete=models.CASCADE,related_name='product_comment')
    comment=models.ForeignKey('self',on_delete=models.CASCADE,related_name='comments')
    is_reply=models.BooleanField(default=False)
    body=models.TextField(max_length=400)
    
    def __str__(self) -> str:
        return f'{self.user}-{self.body}'