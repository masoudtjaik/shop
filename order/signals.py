from django.db.models.signals import post_save, pre_delete, pre_save
from .models import Order, OrderItem
from django.dispatch import receiver


@receiver(post_save, sender=OrderItem)
def total_new(sender, **kwargs):
    # if kwargs['created']:
    kwargs['instance'].order.total = 0
    kwargs['instance'].order.total += kwargs['instance'].get_count()
    # kwargs['instance'].product.inventory -=kwargs['instance'].count

    post_save.disconnect(total_new, sender=OrderItem)
    kwargs['instance'].product.save()
    kwargs['instance'].order.save()
    post_save.connect(total_new, sender=OrderItem)


@receiver(post_save, sender=Order)
def total_order(sender, **kwargs):
    kwargs['instance'].total = 0
    kwargs['instance'].total = kwargs['instance'].total_price()
    if kwargs['instance'].discount:
        if kwargs['instance'].discount.type == 'number':
            if kwargs['instance'].discount.amount > kwargs['instance'].total:
                kwargs['instance'].total = 0
            else:
                kwargs['instance'].total -= kwargs['instance'].discount.amount
        elif kwargs['instance'].discount.type == 'perecent':
            kwargs['instance'].total = kwargs['instance'].total - (kwargs['instance'].total * kwargs[
                'instance'].discount.amount) / 100

    post_save.disconnect(total_order, sender=Order)
    kwargs['instance'].save()
    post_save.connect(total_order, sender=Order)


@receiver(pre_save, sender=OrderItem)
def counter_quantity(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = sender.objects.get(pk=instance.pk)
        instance.product.inventory -= (instance.count - previous_instance.count)
    else:
        instance.product.inventory -= instance.count
    instance.product.save()
