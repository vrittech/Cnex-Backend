from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def ProductPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=Product)
def ProductPreSave(sender,instance,**kwargs):
    if instance.is_stock == True:
        instance.product_type = "regular"
    else:
        instance.product_type = "pre-order"
    
    if instance.is_deleted == True:
        instance.is_publish = False




         

