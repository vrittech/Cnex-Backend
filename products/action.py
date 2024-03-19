from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def ProductPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=Product)
def ProductPreSave(sender,instance,**kwargs):
    pass

