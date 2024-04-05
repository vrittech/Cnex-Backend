from django.db import models
from order.models import Order
from appointment.models import CheckoutAppointment

# Create your models here.
class Payment(models.Model): #payment products
    order = models.ForeignKey(Order,related_name = "payment",on_delete = models.SET_NULL,null = True)
    ammount = models.FloatField()
    payment_mode = models.CharField(max_length = 100,choices = (('khalti','Khalti'),('esewa','Esewa'),('cod','Cash On Ddelivery')))
    refrence_id = models.CharField(max_length = 4000,unique = True)
    remarks = models.CharField(max_length = 3000,null = True,blank = True)
    status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('unpaid','Paid'),
        ('half', 'Half Payment'),
        ('cod','Cash On Delivery'),
        ('refunded','Refunded'),
    ],)

class PaymentFail(models.Model):
    order = models.ForeignKey(Order,related_name = "payment_fail",on_delete = models.SET_NULL,null = True)
    payment_mode = models.CharField(max_length = 100,choices = (('khalti','Khalti'),('esewa','Esewa'),('cod','Cash On Ddelivery')))
    refrence_id = models.CharField(max_length = 4000)
    services_product = models.CharField(max_length = 100)
    server_response = models.CharField(max_length = 3000,null = True,blank = True)

class PaymentService(models.Model):
    order = models.ForeignKey(CheckoutAppointment,related_name = "payment",on_delete = models.SET_NULL,null = True)
    ammount = models.FloatField()
    payment_mode = models.CharField(max_length = 100,choices = (('khalti','Khalti'),('esewa','Esewa'),('cod','Cash On Ddelivery')))
    refrence_id = models.CharField(max_length = 4000,unique = True)
    remarks = models.CharField(max_length = 3000,null = True,blank = True)
    status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('unpaid','Paid'),
        ('half', 'Half Payment'),
        ('cod','Cash On Delivery'),
        ('refunded','Refunded'),
    ],)