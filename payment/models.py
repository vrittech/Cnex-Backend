from django.db import models
from order.models import Order

# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Order,related_name = "payment",on_delete = models.PROTECT)
    ammount = models.FloatField()
    payment_mode = models.CharField(max_length = 100,choices = (('khalti','Khalti'),('esewa','Esewa'),('cod','Cash On Ddelivery')))
    refrence_id = models.CharField(max_length = 4000,default = 'cod')
    remarks = models.CharField(max_length = 3000,null = True,blank = True)
    status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('unpaid','Paid'),
        ('half', 'Half Payment'),
        ('cod','Cash On Delivery'),
        ('refunded','Refunded'),
    ],)