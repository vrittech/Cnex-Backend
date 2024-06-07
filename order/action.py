from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Order,OrderItem,Cart
from products.models import Product
from notification.handle_notification import NotificationHandler
from .utilities.quantity_manage import quantityManage


@receiver(post_save, sender=Order)
def OrderPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=Order)
def OrderPreSave(sender,instance,**kwargs):
    if instance.pk:
        if instance.order_status == 'delivered' and instance.order_status != Order.objects.get(id = instance.id).order_status:
            try:
                NotificationHandler(instance,"order_delivered")
            except:
                print("issues in notifications.")
        
        if instance.order_status not in ["checkout","cancelled"] and Order.objects.get(id = instance.id).order_status in ["checkout","cancelled"]:
            quantityManage(instance,'-')

        elif instance.order_status in ["checkout","cancelled"] and Order.objects.get(id = instance.id).order_status not in ["checkout","cancelled"]:
            quantityManage(instance,'+')

@receiver(pre_save,sender=OrderItem)
def OrderItemPreSave(sender,instance,**kwargs):
    pass

