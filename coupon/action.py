from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Order,OrderItem,Cart
from products.models import Product
from notification.handle_notification import NotificationHandler


@receiver(post_save, sender=Order)
def OrderPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=Order)
def OrderPreSave(sender,instance,**kwargs):
    if instance.pk:
        if instance.order_status == 'delivered' and instance.order_status != Order.objects.get(id = instance.id).order_status:
            NotificationHandler(instance,"order_delivered")

    #
@receiver(post_save, sender=OrderItem)
def OrderItemPostSave(sender, instance, created, **kwargs):
    if created:
        chanages_quantity = instance.product.quantity - instance.quantity
        if chanages_quantity>0:
            Product.objects.filter(id = instance.product.id).update(quantity = chanages_quantity)
        else:
            Product.objects.filter(id = instance.product.id).update(quantity = 0,product_type =  "pre-order")

@receiver(pre_save,sender=OrderItem)
def OrderItemPreSave(sender,instance,**kwargs):
    pass

