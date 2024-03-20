from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Order,OrderItem


@receiver(post_save, sender=Order)
def OrderPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=Order)
def OrderPreSave(sender,instance,**kwargs):
    pass

@receiver(post_save, sender=OrderItem)
def OrderItemPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=OrderItem)
def OrderItemPreSave(sender,instance,**kwargs):
    
    pass


