from django.db.models.signals import pre_save,post_save , pre_delete
from django.dispatch import receiver
from .models import Payment,PaymentService
from order.models import Order
from appointment.models import Appointment,CheckoutAppointment
from notification.handle_notification import NotificationHandler


@receiver(post_save, sender=Payment)
def PaymentPostSave(sender, instance, created, **kwargs):
    if created:
        order_obj = Order.objects.filter(id = instance.order_id)
        if order_obj.exists():
            payment_status = "unpaid"
            if order_obj.first().order_items.all().count() == 1 and order_obj.first().order_items.all().first().product.product_type == "pre-order":
                if instance.ammount == order_obj.first().total_price:
                    payment_status = "paid"
                else:
                    payment_status = "half"   
            else:
                if order_obj.first().total_price == instance.ammount:
                    payment_status = "paid"
                    try:
                        NotificationHandler(order_obj.first(),"payment_confirmed")
                    except:
                        print("notification fail for payment confirmed.")
              
                else:
                    payment_status = "unpaid"
            order_obj.first().save(payment_status = payment_status,order_status = "in-progress")
    

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
        
        try:
            service_name = instance.order.services_items.first().service.name
            slots_obj = instance.order.services_items.first().slots.first()
            slots_from_time = slots_obj.from_time
            slots_to_time = slots_obj.to_time
            number_of_staffs = slots_obj.number_of_staffs
        except:
            service_name = ''
            slots_from_time =  ''
            slots_to_time = ''
            number_of_staffs = ''

        payload =  {
            'user':instance.order.user,
            'checkout_appointment':instance.order,
            'payment_amount':instance.order.total_price,
            'payment_status':payment_status,
            'appointment_status':'confirmed',
            'payment_mode':instance.payment_mode,

            'service_name':service_name,
            'slots_from_time':slots_from_time,
            'slots_to_time':slots_to_time,
            'number_of_staffs':number_of_staffs

        }
        Appointment.objects.create(**payload)
        try:
            NotificationHandler(instance.order,"service_booked")
        except:
            pass #notificaation hide if error
    

@receiver(pre_save,sender=PaymentService)
def PaymentServicePreSave(sender,instance,**kwargs):
    pass


