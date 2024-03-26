from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Payment
from order.models import Order


@receiver(post_save, sender=Payment)
def PaymentPostSave(sender, instance, created, **kwargs):
    if instance.created:
        Order.objects.filter(id = instance.order_id).update(payment_status = "paid")
    

@receiver(pre_save,sender=Payment)
def PaymentPreSave(sender,instance,**kwargs):
    pass

