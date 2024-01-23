from django.db import models
from datetime import datetime,timedelta
from django.utils import timezone
# Create your models here.
class CustomBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True
        
#--------------------------------------------------
#User
class QuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class Manager(models.Manager):

    def get_queryset(self):
        return QuerySet(self.model).filter(is_deleted=False)

    def archive(self):
        return QuerySet(self.model)
    
    def ten_product_new(self):
        return QuerySet(self.model).select_related('category').filter(is_deleted=False, is_active=True)[:10]
    
    def ten_is_discount(self):
        return QuerySet(self.model).filter(is_deleted=False,is_active=True,discount__isnull=False)[:10]
    
    # def get_count(self):
    #     # print('hello',self.model.is_deleted)
    #     return QuerySet(self.model).get(pk=self.id)
    
    def deleted(self):
        return QuerySet(self.model).filter(is_deleted=True)



class Base(CustomBase):
    is_active = models.BooleanField(default=True)
    objects = Manager()

    class Meta:
        abstract = True
        ordering = ('-created_at',)
    
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()

    def __str__(self) -> str:
        return f'{self.created_at}'


class StatusMixin:
    @property
    def status(self) -> bool:
        return self.is_active and not self.is_deleted  # noqa
#--------------------------------------------------

#Discount manager
class DiscountQuerySet(models.QuerySet):
    
    def start_date(self):
          if datetime.today>=self.start:
              return super().update(is_active=True)
    
    def end_date(self):
         if self.expire<datetime.today:
            return super().update(is_deleted=True)
    
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()
    
class DiscountManager(models.Manager):

    def get_queryset(self):
        return DiscountQuerySet(self.model).filter(is_deleted=False,expire__gte=datetime.today())

    def archive(self):
        return DiscountQuerySet(self.model)
    

    def deleted(self):
        return DiscountQuerySet(self.model).filter(is_deleted=True)

class BaseDiscount(CustomBase):
    start=models.DateTimeField(default=timezone.now()+timedelta(minutes=10))
    expire=models.DateTimeField(default=timezone.now()+timedelta(days=1,minutes=10))
    is_active=models.BooleanField(default=True)
    objects=DiscountManager()
    
    class Meta:
        abstract = True
        ordering = ('-start',)
        
    
    def start_discount(self):
          if datetime.today>=self.start:
              self.is_active=True
              self.save()
    
    def end_discount(self):
         if self.end<datetime.today:
            self.is_delete=True
            self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()
#--------------------------------------------------
#Order manager 
class OrderQuerySet(models.QuerySet):
    
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()
    
class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderQuerySet(self.model).filter(is_deleted=False,)

    def archive(self):
        return OrderQuerySet(self.model)
    
    def paid(self):
        return OrderQuerySet(self.model).filter(id_deleted=False,is_paid=True)
    
        
    
    def unpaid(self):
        return OrderQuerySet(self.model).filter(id_deleted=False,is_paid=False)

    def deleted(self):
        return OrderQuerySet(self.model).filter(is_deleted=True)

class BaseOrder(CustomBase):
    is_paid=models.BooleanField(default=False)
    objects=OrderManager()
    
    class Meta:
        abstract = True
        ordering = ('-created_at',)
        
    
    def paid(self):
            self.is_paid=True
            self.save()
    
    def unpaid(self):
            self.is_paid=False
            self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()