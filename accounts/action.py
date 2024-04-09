from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import CustomUser,ShippingAddress

@receiver(post_save, sender=ShippingAddress)
def ShippingAddressPostSave(sender, instance, created, **kwargs):
    pass

@receiver(pre_save,sender=ShippingAddress)
def ShippingAddressPreSave(sender,instance,**kwargs):
    all_shipping_address = instance.profile.shipping_address.all().filter(is_default = True)
    all_shipping_address.update(is_default = False) #change  other is_default True to False

@receiver(post_save, sender=CustomUser)
def CustomUserPostSave(sender, instance, created, **kwargs):
    if not created:
        print("notification here")

@receiver(pre_save, sender=CustomUser)
def CustomUserPreSave(sender, instance, **kwargs):
    pass