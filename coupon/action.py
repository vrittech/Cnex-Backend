from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Coupon
from notification.handle_notification import NotificationHandler


@receiver(post_save, sender=Coupon)
def CouponPostSave(sender, instance, created, **kwargs):
    if created:
        NotificationHandler(instance,"new_coupon")