from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Payment,PaymentService
from order.models import Order
from appointment.models import Appointment,CheckoutAppointment


@receiver(post_save, sender=Payment)
def PaymentPostSave(sender, instance, created, **kwargs):
    if created:
        order_obj = Order.objects.filter(id = instance.order_id)
        if order_obj.exists():
            payment_status = "unpaid"
            if order_obj.first().order_items.all().count() == 1 and order_obj.first().order_items.all().first().product.product_type == "pre-order":
                print(" this order is pre order")
                if instance.ammount == order_obj.first().total_price:
                    print("half payment")
                    payment_status = "paid"
                else:
                    payment_status = "half"   
                    print("half payment")             
            else:
                print(" this order is regular order")
                if order_obj.first().total_price == instance.ammount:
                    payment_status = "paid"
                else:
                    payment_status = "unpaid"
            order_obj.update(payment_status = payment_status,order_status = "in-progress")
    

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
        Appointment.objects.create(**payload)
    

@receiver(pre_save,sender=PaymentService)
def PaymentServicePreSave(sender,instance,**kwargs):
    pass


