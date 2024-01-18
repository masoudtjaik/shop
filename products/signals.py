from django.db.models.signals import post_save, pre_delete
from .models import Product
from django.dispatch import receiver


@receiver(post_save, sender=Product)
def total(sender, **kwargs):
    # if kwargs['created']:
    if kwargs['instance'].discount:
        if kwargs['instance'].discount.type == 'number':
            if kwargs['instance'].price > kwargs['instance'].discount.amount:
                kwargs['instance'].price_discount = kwargs['instance'].price - kwargs['instance'].discount.amount
        elif kwargs['instance'].discount.type == 'perecent':
            price = (kwargs['instance'].price * kwargs['instance'].discount.amount) / 100
            if kwargs['instance'].discount.max_amount and price > kwargs['instance'].discount.max_amount:
                kwargs['instance'].price_discount = kwargs['instance'].price - kwargs['instance'].discount.max_amount
            else:
                kwargs['instance'].price_discount = kwargs['instance'].price - price
    else:
        kwargs['instance'].price_discount = kwargs['instance'].price
    post_save.disconnect(total, sender=Product)
    kwargs['instance'].save()
    post_save.connect(total, sender=Product)

# post_save.connect(receiver=total, sender=Product)
