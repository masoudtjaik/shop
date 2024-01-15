from django.db.models.signals import  post_save,pre_delete
from .models import Order,OrderItem
from django.dispatch import receiver


# @receiver(post_save,sender=Order)
def total(sender,**kwargs):
    if kwargs['created']:
        kwargs['instance'].order.total += kwargs['instance'].get_count()
        kwargs['instance'].product.inventory -=kwargs['instance'].count
        if kwargs['instance'].order.discount:
           if  kwargs['instance'].order.discount.type=='number' :
               if kwargs['instance'].order.discount.amount>kwargs['instance'].order.total:
                   kwargs['instance'].order.total=0
               else:
                    kwargs['instance'].order.total -=kwargs['instance'].order.discount.amount
           elif  kwargs['instance'].order.discount.type=='perecent' :
               kwargs['instance'].order.total = (kwargs['instance'].order.total* kwargs['instance'].order.discount.amount)/100
        kwargs['instance'].product.save()
        kwargs['instance'].order.save()
post_save.connect(receiver=total,sender=OrderItem)
# @receiver(post_save,sender=Order)
# def total_order(sender,**kwargs):
#     if kwargs['created']:
#         print('created')
           
#         kwargs['instance'].save()
# @receiver(pre_delete,sender=Order)
def delete(sender,**kwargs):
    print('delete done')
    kwargs['instance'].order_orderitem.product.inventory +=kwargs['instance'].count
    kwargs['instance'].order_orderitem.product.save()

pre_delete.connect(receiver=delete,sender=Order)