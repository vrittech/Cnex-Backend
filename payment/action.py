from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Payment,PaymentService
from order.models import Order
from appointment.models import Appointment,CheckoutAppointment


@receiver(post_save, sender=Payment)
def PaymentPostSave(sender, instance, created, **kwargs):
    if created:
        Order.objects.filter(id = instance.order_id).update(payment_status = "paid",order_status = "in-progress")
    

@receiver(pre_save,sender=Payment)
def PaymentPreSave(sender,instance,**kwargs):
    pass



@receiver(post_save, sender=PaymentService)
def PaymentServicePostSave(sender, instance, created, **kwargs):
    if created:
        if instance.order.total_price == instance.ammount:
            payment_status = 'paid'
        else:
            payment_status =  "unpaid"
        
        payload =  {
            'user':instance.order.user,
            'checkout_appointment':instance.order,
            'payment_amount':instance.order.total_price,
            'payment_status':payment_status,
            'appointment_status':'confirmed',
            'payment_mode':instance.payment_mode,
        }
        Appointment.objects.create(payload)
    

@receiver(pre_save,sender=PaymentService)
def PaymentServicePreSave(sender,instance,**kwargs):
    pass


